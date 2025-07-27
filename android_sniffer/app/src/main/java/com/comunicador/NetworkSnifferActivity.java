package com.comunicador;

import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.net.ConnectivityManager;
import android.net.Network;
import android.net.NetworkCapabilities;
import android.net.NetworkInfo;
import android.net.wifi.WifiConfiguration;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class NetworkSnifferActivity extends AppCompatActivity {
    
    private static final String TAG = "NetworkSniffer";
    private static final int TARGET_BANDWIDTH_MB = 30;
    private static final int PERMISSION_REQUEST_CODE = 1001;
    
    // UI Elements
    private TextView statusText;
    private TextView bandwidthText;
    private TextView networksText;
    private ProgressBar bandwidthProgress;
    private Button sendButton;
    
    // Network Components
    private NetworkSniffer networkSniffer;
    private BandwidthAccumulator bandwidthAccumulator;
    private MessageQueue messageQueue;
    
    // Threading
    private ExecutorService executorService;
    private Handler mainHandler;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_network_sniffer);
        
        initializeComponents();
        requestPermissions();
        setupUI();
        startNetworkSniffer();
    }
    
    private void initializeComponents() {
        // UI
        statusText = findViewById(R.id.statusText);
        bandwidthText = findViewById(R.id.bandwidthText);
        networksText = findViewById(R.id.networksText);
        bandwidthProgress = findViewById(R.id.bandwidthProgress);
        sendButton = findViewById(R.id.sendButton);
        
        // Threading
        executorService = Executors.newCachedThreadPool();
        mainHandler = new Handler(Looper.getMainLooper());
        
        // Network Components
        networkSniffer = new NetworkSniffer(this);
        bandwidthAccumulator = new BandwidthAccumulator(TARGET_BANDWIDTH_MB);
        messageQueue = new MessageQueue();
        
        Log.i(TAG, "🚀 Network Sniffer iniciado - Procurando por " + TARGET_BANDWIDTH_MB + "MB");
    }
    
    private void setupUI() {
        bandwidthProgress.setMax(TARGET_BANDWIDTH_MB);
        bandwidthProgress.setProgress(0);
        
        sendButton.setOnClickListener(v -> {
            if (bandwidthAccumulator.hasEnoughBandwidth()) {
                startMessageDelivery();
            } else {
                Toast.makeText(this, "Ainda coletando banda: " + 
                    bandwidthAccumulator.getCurrentBandwidth() + "MB/" + TARGET_BANDWIDTH_MB + "MB", 
                    Toast.LENGTH_SHORT).show();
            }
        });
        
        updateUI();
    }
    
    private void requestPermissions() {
        String[] permissions = {
            Manifest.permission.ACCESS_WIFI_STATE,
            Manifest.permission.CHANGE_WIFI_STATE,
            Manifest.permission.ACCESS_NETWORK_STATE,
            Manifest.permission.CHANGE_NETWORK_STATE,
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.ACCESS_COARSE_LOCATION,
            Manifest.permission.INTERNET
        };
        
        List<String> permissionsToRequest = new ArrayList<>();
        for (String permission : permissions) {
            if (ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED) {
                permissionsToRequest.add(permission);
            }
        }
        
        if (!permissionsToRequest.isEmpty()) {
            ActivityCompat.requestPermissions(this, 
                permissionsToRequest.toArray(new String[0]), 
                PERMISSION_REQUEST_CODE);
        }
    }
    
    private void startNetworkSniffer() {
        executorService.execute(() -> {
            while (!Thread.currentThread().isInterrupted()) {
                try {
                    // Varre redes disponíveis
                    List<NetworkAnchor> availableNetworks = networkSniffer.scanAvailableNetworks();
                    
                    for (NetworkAnchor network : availableNetworks) {
                        // Tenta se ancorar superficialmente
                        if (networkSniffer.trySuperficialAnchor(network)) {
                            
                            // Mede banda disponível rapidamente
                            double bandwidthMB = networkSniffer.measureBandwidth(network);
                            
                            if (bandwidthMB > 0) {
                                bandwidthAccumulator.addBandwidth(bandwidthMB, network);
                                
                                mainHandler.post(() -> {
                                    updateUI();
                                    Log.d(TAG, String.format("🔗 Ancorado em %s: +%.2fMB (Total: %.2fMB)", 
                                        network.getNetworkName(), bandwidthMB, 
                                        bandwidthAccumulator.getCurrentBandwidth()));
                                });
                                
                                // Verifica se já tem banda suficiente
                                if (bandwidthAccumulator.hasEnoughBandwidth()) {
                                    mainHandler.post(() -> {
                                        Toast.makeText(NetworkSnifferActivity.this, 
                                            "✅ Banda suficiente coletada! Pronto para enviar.", 
                                            Toast.LENGTH_LONG).show();
                                        sendButton.setEnabled(true);
                                    });
                                    break;
                                }
                            }
                            
                            // Desancora para economizar bateria
                            networkSniffer.releaseAnchor(network);
                        }
                    }
                    
                    // Pausa antes da próxima varredura
                    Thread.sleep(5000); // 5 segundos
                    
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                } catch (Exception e) {
                    Log.e(TAG, "Erro durante varredura: " + e.getMessage(), e);
                }
            }
        });
    }
    
    private void updateUI() {
        double currentBandwidth = bandwidthAccumulator.getCurrentBandwidth();
        List<NetworkAnchor> anchoredNetworks = bandwidthAccumulator.getAnchoredNetworks();
        
        statusText.setText(bandwidthAccumulator.hasEnoughBandwidth() ? 
            "✅ Pronto para enviar" : "🔍 Coletando banda...");
            
        bandwidthText.setText(String.format("%.2fMB / %dMB", currentBandwidth, TARGET_BANDWIDTH_MB));
        
        bandwidthProgress.setProgress((int) currentBandwidth);
        
        StringBuilder networksList = new StringBuilder("Redes ancoradas:\n");
        for (NetworkAnchor anchor : anchoredNetworks) {
            networksList.append(String.format("• %s: %.2fMB\n", 
                anchor.getNetworkName(), anchor.getContributedBandwidth()));
        }
        networksText.setText(networksList.toString());
        
        sendButton.setEnabled(bandwidthAccumulator.hasEnoughBandwidth());
    }
    
    private void startMessageDelivery() {
        Toast.makeText(this, "🚀 Iniciando entrega usando banda acumulada...", Toast.LENGTH_SHORT).show();
        
        executorService.execute(() -> {
            try {
                // Usa as âncoras coletadas para enviar a mensagem
                List<NetworkAnchor> anchors = bandwidthAccumulator.getAnchoredNetworks();
                MessageDelivery delivery = new MessageDelivery(anchors);
                
                boolean success = delivery.sendPendingMessages(messageQueue.getAllMessages());
                
                mainHandler.post(() -> {
                    if (success) {
                        Toast.makeText(this, "✅ Mensagem enviada com sucesso!", Toast.LENGTH_LONG).show();
                        // Reseta o acumulador
                        bandwidthAccumulator.reset();
                        updateUI();
                    } else {
                        Toast.makeText(this, "❌ Falha no envio. Continuando coleta...", Toast.LENGTH_SHORT).show();
                    }
                });
                
            } catch (Exception e) {
                Log.e(TAG, "Erro durante entrega: " + e.getMessage(), e);
                mainHandler.post(() -> 
                    Toast.makeText(this, "Erro: " + e.getMessage(), Toast.LENGTH_SHORT).show());
            }
        });
    }
    
    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (executorService != null) {
            executorService.shutdown();
        }
        if (networkSniffer != null) {
            networkSniffer.cleanup();
        }
    }
    
    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        
        if (requestCode == PERMISSION_REQUEST_CODE) {
            boolean allGranted = true;
            for (int result : grantResults) {
                if (result != PackageManager.PERMISSION_GRANTED) {
                    allGranted = false;
                    break;
                }
            }
            
            if (!allGranted) {
                Toast.makeText(this, "⚠️ Permissões necessárias para funcionamento completo", 
                    Toast.LENGTH_LONG).show();
            }
        }
    }
}
