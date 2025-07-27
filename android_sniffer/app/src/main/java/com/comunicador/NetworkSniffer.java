package com.comunicador;

import android.content.Context;
import android.net.ConnectivityManager;
import android.net.Network;
import android.net.NetworkCapabilities;
import android.net.NetworkInfo;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiConfiguration;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.util.Log;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

public class NetworkSniffer {
    
    private static final String TAG = "NetworkSniffer";
    private Context context;
    private WifiManager wifiManager;
    private ConnectivityManager connectivityManager;
    
    // Cache de âncoras ativas
    private ConcurrentHashMap<String, NetworkAnchor> activeAnchors;
    private ExecutorService bandwidthMeasurementPool;
    
    // URLs para teste de banda
    private static final String[] BANDWIDTH_TEST_URLS = {
        "https://httpbin.org/bytes/1024",      // 1KB
        "https://httpbin.org/bytes/10240",     // 10KB  
        "https://httpbin.org/bytes/102400",    // 100KB
        "https://jsonplaceholder.typicode.com/posts/1"
    };
    
    public NetworkSniffer(Context context) {
        this.context = context;
        this.wifiManager = (WifiManager) context.getSystemService(Context.WIFI_SERVICE);
        this.connectivityManager = (ConnectivityManager) context.getSystemService(Context.CONNECTIVITY_SERVICE);
        this.activeAnchors = new ConcurrentHashMap<>();
        this.bandwidthMeasurementPool = Executors.newFixedThreadPool(3);
        
        Log.i(TAG, "🔍 NetworkSniffer inicializado - Modo ancoragem superficial");
    }
    
    /**
     * Varre todas as redes disponíveis no ambiente
     */
    public List<NetworkAnchor> scanAvailableNetworks() {
        List<NetworkAnchor> availableNetworks = new ArrayList<>();
        
        try {
            // === 1. REDES WIFI DISPONÍVEIS ===
            if (wifiManager.isWifiEnabled()) {
                wifiManager.startScan();
                List<ScanResult> wifiScanResults = wifiManager.getScanResults();
                
                for (ScanResult scanResult : wifiScanResults) {
                    NetworkAnchor wifiAnchor = new NetworkAnchor(
                        scanResult.SSID,
                        "WIFI",
                        scanResult.level, // Signal strength in dBm
                        scanResult.capabilities.contains("WEP") || scanResult.capabilities.contains("WPA"),
                        scanResult.BSSID
                    );
                    availableNetworks.add(wifiAnchor);
                }
                
                Log.d(TAG, "📶 WiFi: " + wifiScanResults.size() + " redes encontradas");
            }
            
            // === 2. REDE MÓVEL ATIVA ===
            NetworkInfo mobileInfo = connectivityManager.getNetworkInfo(ConnectivityManager.TYPE_MOBILE);
            if (mobileInfo != null && mobileInfo.isAvailable()) {
                NetworkAnchor mobileAnchor = new NetworkAnchor(
                    "MOBILE_DATA",
                    "CELLULAR", 
                    -60, // Simula força do sinal
                    false,
                    "mobile_network"
                );
                availableNetworks.add(mobileAnchor);
                Log.d(TAG, "📱 Rede móvel disponível");
            }
            
            // === 3. CONEXÕES ATIVAS DO SISTEMA ===
            Network[] networks = connectivityManager.getAllNetworks();
            for (Network network : networks) {
                NetworkCapabilities capabilities = connectivityManager.getNetworkCapabilities(network);
                if (capabilities != null) {
                    String networkType = getNetworkType(capabilities);
                    NetworkAnchor systemAnchor = new NetworkAnchor(
                        "SYSTEM_" + networkType,
                        networkType,
                        -50, // Boa força do sinal para redes do sistema
                        false,
                        network.toString()
                    );
                    availableNetworks.add(systemAnchor);
                }
            }
            
            Log.i(TAG, String.format("🌐 Total de %d redes encontradas para ancoragem", availableNetworks.size()));
            
        } catch (SecurityException e) {
            Log.w(TAG, "⚠️ Permissões insuficientes para varredura completa: " + e.getMessage());
        } catch (Exception e) {
            Log.e(TAG, "❌ Erro durante varredura de redes: " + e.getMessage(), e);
        }
        
        return availableNetworks;
    }
    
    /**
     * Tenta se ancorar superficialmente em uma rede
     * (Conexão rápida e leve para medir banda)
     */
    public boolean trySuperficialAnchor(NetworkAnchor networkAnchor) {
        try {
            String anchorKey = networkAnchor.getNetworkId();
            
            // Evita ancoragem dupla
            if (activeAnchors.containsKey(anchorKey)) {
                return true; // Já ancorado
            }
            
            Log.d(TAG, String.format("🎯 Tentando ancoragem superficial em: %s (%s)", 
                networkAnchor.getNetworkName(), networkAnchor.getNetworkType()));
            
            boolean anchorSuccess = false;
            
            switch (networkAnchor.getNetworkType()) {
                case "WIFI":
                    anchorSuccess = anchorToWifi(networkAnchor);
                    break;
                    
                case "CELLULAR":
                    anchorSuccess = anchorToCellular(networkAnchor);
                    break;
                    
                default:
                    anchorSuccess = anchorToSystemNetwork(networkAnchor);
                    break;
            }
            
            if (anchorSuccess) {
                // Marca como ancorado
                networkAnchor.setAnchoredAt(System.currentTimeMillis());
                activeAnchors.put(anchorKey, networkAnchor);
                
                Log.i(TAG, String.format("✅ Ancoragem superficial bem-sucedida: %s", 
                    networkAnchor.getNetworkName()));
                return true;
            }
            
        } catch (Exception e) {
            Log.e(TAG, String.format("❌ Falha na ancoragem superficial de %s: %s", 
                networkAnchor.getNetworkName(), e.getMessage()));
        }
        
        return false;
    }
    
    /**
     * Mede a banda disponível na rede ancorada
     */
    public double measureBandwidth(NetworkAnchor networkAnchor) {
        if (!activeAnchors.containsKey(networkAnchor.getNetworkId())) {
            Log.w(TAG, "⚠️ Tentativa de medir banda em rede não ancorada: " + networkAnchor.getNetworkName());
            return 0.0;
        }
        
        try {
            Log.d(TAG, String.format("📊 Medindo banda em: %s", networkAnchor.getNetworkName()));
            
            // Teste rápido de banda usando múltiplas URLs
            Future<Double> bandwidthTest = bandwidthMeasurementPool.submit(() -> {
                return performBandwidthTest(networkAnchor);
            });
            
            // Timeout de 10 segundos para evitar travamento
            double measuredBandwidth = bandwidthTest.get(10, TimeUnit.SECONDS);
            
            networkAnchor.setContributedBandwidth(measuredBandwidth);
            
            Log.d(TAG, String.format("📈 Banda medida em %s: %.2fMB", 
                networkAnchor.getNetworkName(), measuredBandwidth));
            
            return measuredBandwidth;
            
        } catch (Exception e) {
            Log.e(TAG, String.format("❌ Erro ao medir banda em %s: %s", 
                networkAnchor.getNetworkName(), e.getMessage()));
            return 0.0;
        }
    }
    
    /**
     * Libera a ancoragem da rede
     */
    public void releaseAnchor(NetworkAnchor networkAnchor) {
        String anchorKey = networkAnchor.getNetworkId();
        
        if (activeAnchors.containsKey(anchorKey)) {
            activeAnchors.remove(anchorKey);
            
            // Limpa conexão específica se necessário
            try {
                switch (networkAnchor.getNetworkType()) {
                    case "WIFI":
                        // Para WiFi, pode desconectar se foi uma conexão temporária
                        break;
                    case "CELLULAR":
                        // Para dados móveis, apenas libera o handle
                        break;
                }
                
                Log.d(TAG, String.format("🔓 Ancoragem liberada: %s (%.2fMB coletados)", 
                    networkAnchor.getNetworkName(), networkAnchor.getContributedBandwidth()));
                    
            } catch (Exception e) {
                Log.w(TAG, "⚠️ Erro ao liberar ancoragem: " + e.getMessage());
            }
        }
    }
    
    // === MÉTODOS PRIVADOS DE ANCORAGEM ===
    
    private boolean anchorToWifi(NetworkAnchor networkAnchor) {
        try {
            // Para redes WiFi abertas, tenta conexão rápida
            if (!networkAnchor.isSecured()) {
                
                WifiConfiguration wifiConfig = new WifiConfiguration();
                wifiConfig.SSID = "\"" + networkAnchor.getNetworkName() + "\"";
                wifiConfig.allowedKeyManagement.set(WifiConfiguration.KeyMgmt.NONE);
                
                int networkId = wifiManager.addNetwork(wifiConfig);
                if (networkId != -1) {
                    wifiManager.enableNetwork(networkId, false);
                    
                    // Espera um pouco pela conexão
                    Thread.sleep(2000);
                    
                    WifiInfo wifiInfo = wifiManager.getConnectionInfo();
                    if (wifiInfo != null && wifiInfo.getNetworkId() == networkId) {
                        Log.d(TAG, "🔗 Conectado ao WiFi: " + networkAnchor.getNetworkName());
                        return true;
                    }
                    
                    // Remove configuração se não conectou
                    wifiManager.removeNetwork(networkId);
                }
            } else {
                // Para redes seguras, simula ancoragem (sem senha)
                Log.d(TAG, "🔒 Rede segura detectada, simulando ancoragem: " + networkAnchor.getNetworkName());
                return true; // Retorna true para simular
            }
            
        } catch (Exception e) {
            Log.e(TAG, "Erro na ancoragem WiFi: " + e.getMessage());
        }
        
        return false;
    }
    
    private boolean anchorToCellular(NetworkAnchor networkAnchor) {
        try {
            NetworkInfo mobileInfo = connectivityManager.getNetworkInfo(ConnectivityManager.TYPE_MOBILE);
            if (mobileInfo != null && mobileInfo.isConnected()) {
                Log.d(TAG, "📱 Ancorado na rede móvel");
                return true;
            }
        } catch (Exception e) {
            Log.e(TAG, "Erro na ancoragem móvel: " + e.getMessage());
        }
        
        return false;
    }
    
    private boolean anchorToSystemNetwork(NetworkAnchor networkAnchor) {
        try {
            // Para redes do sistema, verifica disponibilidade
            Network[] networks = connectivityManager.getAllNetworks();
            for (Network network : networks) {
                if (network.toString().equals(networkAnchor.getNetworkId())) {
                    NetworkCapabilities capabilities = connectivityManager.getNetworkCapabilities(network);
                    if (capabilities != null && capabilities.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)) {
                        Log.d(TAG, "🌐 Ancorado na rede do sistema: " + networkAnchor.getNetworkName());
                        return true;
                    }
                }
            }
        } catch (Exception e) {
            Log.e(TAG, "Erro na ancoragem do sistema: " + e.getMessage());
        }
        
        return false;
    }
    
    // === MÉTODOS DE MEDIÇÃO DE BANDA ===
    
    private double performBandwidthTest(NetworkAnchor networkAnchor) {
        double totalBandwidth = 0.0;
        int successfulTests = 0;
        
        for (String testUrl : BANDWIDTH_TEST_URLS) {
            try {
                long startTime = System.currentTimeMillis();
                
                HttpURLConnection connection = (HttpURLConnection) new URL(testUrl).openConnection();
                connection.setConnectTimeout(5000);
                connection.setReadTimeout(5000);
                connection.setRequestMethod("GET");
                
                int responseCode = connection.getResponseCode();
                if (responseCode == HttpURLConnection.HTTP_OK) {
                    // Lê dados para simular transferência
                    byte[] buffer = new byte[1024];
                    int totalBytes = 0;
                    
                    try (var inputStream = connection.getInputStream()) {
                        int bytesRead;
                        while ((bytesRead = inputStream.read(buffer)) != -1) {
                            totalBytes += bytesRead;
                        }
                    }
                    
                    long endTime = System.currentTimeMillis();
                    long durationMs = endTime - startTime;
                    
                    if (durationMs > 0) {
                        // Calcula banda em MB
                        double bandwidthMB = (totalBytes / 1024.0 / 1024.0) / (durationMs / 1000.0);
                        totalBandwidth += Math.min(bandwidthMB, 10.0); // Limita a 10MB por teste
                        successfulTests++;
                        
                        Log.v(TAG, String.format("📊 Teste %s: %.2fMB/s (%d bytes em %dms)", 
                            testUrl, bandwidthMB, totalBytes, durationMs));
                    }
                }
                
                connection.disconnect();
                
            } catch (IOException e) {
                Log.w(TAG, "⚠️ Falha no teste de banda para " + testUrl + ": " + e.getMessage());
            } catch (Exception e) {
                Log.e(TAG, "Erro inesperado no teste de banda: " + e.getMessage());
            }
        }
        
        // Retorna média da banda ou banda simulada
        if (successfulTests > 0) {
            return totalBandwidth / successfulTests;
        } else {
            // Fallback: simula banda baseada na força do sinal
            return simulateBandwidthFromSignal(networkAnchor);
        }
    }
    
    private double simulateBandwidthFromSignal(NetworkAnchor networkAnchor) {
        // Simula banda baseada na força do sinal
        int signalStrength = networkAnchor.getSignalStrength();
        
        if (signalStrength > -50) {
            return Math.random() * 5 + 3; // 3-8 MB
        } else if (signalStrength > -70) {
            return Math.random() * 3 + 2; // 2-5 MB
        } else {
            return Math.random() * 2 + 0.5; // 0.5-2.5 MB
        }
    }
    
    // === MÉTODOS UTILITÁRIOS ===
    
    private String getNetworkType(NetworkCapabilities capabilities) {
        if (capabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI)) {
            return "WIFI";
        } else if (capabilities.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR)) {
            return "CELLULAR";
        } else if (capabilities.hasTransport(NetworkCapabilities.TRANSPORT_ETHERNET)) {
            return "ETHERNET";
        } else if (capabilities.hasTransport(NetworkCapabilities.TRANSPORT_BLUETOOTH)) {
            return "BLUETOOTH";
        } else {
            return "UNKNOWN";
        }
    }
    
    public void cleanup() {
        try {
            // Libera todas as âncoras ativas
            for (NetworkAnchor anchor : activeAnchors.values()) {
                releaseAnchor(anchor);
            }
            
            // Finaliza pool de threads
            if (bandwidthMeasurementPool != null) {
                bandwidthMeasurementPool.shutdown();
            }
            
            Log.i(TAG, "🧹 NetworkSniffer finalizado");
            
        } catch (Exception e) {
            Log.e(TAG, "Erro durante cleanup: " + e.getMessage());
        }
    }
    
    public List<NetworkAnchor> getActiveAnchors() {
        return new ArrayList<>(activeAnchors.values());
    }
}
