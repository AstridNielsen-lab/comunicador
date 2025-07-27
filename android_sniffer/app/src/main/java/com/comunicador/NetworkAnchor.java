package com.comunicador;

public class NetworkAnchor {
    
    private String networkName;
    private String networkType;
    private int signalStrength;
    private boolean secured;
    private String networkId;
    
    // Dados de ancoragem
    private long anchoredAt;
    private double contributedBandwidth;
    private boolean isActive;
    
    public NetworkAnchor(String networkName, String networkType, int signalStrength, 
                        boolean secured, String networkId) {
        this.networkName = networkName;
        this.networkType = networkType;
        this.signalStrength = signalStrength;
        this.secured = secured;
        this.networkId = networkId;
        this.contributedBandwidth = 0.0;
        this.isActive = false;
        this.anchoredAt = 0;
    }
    
    // Getters e Setters
    public String getNetworkName() {
        return networkName != null ? networkName : "Unknown";
    }
    
    public String getNetworkType() {
        return networkType;
    }
    
    public int getSignalStrength() {
        return signalStrength;
    }
    
    public boolean isSecured() {
        return secured;
    }
    
    public String getNetworkId() {
        return networkId;
    }
    
    public long getAnchoredAt() {
        return anchoredAt;
    }
    
    public void setAnchoredAt(long anchoredAt) {
        this.anchoredAt = anchoredAt;
        this.isActive = true;
    }
    
    public double getContributedBandwidth() {
        return contributedBandwidth;
    }
    
    public void setContributedBandwidth(double contributedBandwidth) {
        this.contributedBandwidth = contributedBandwidth;
    }
    
    public boolean isActive() {
        return isActive;
    }
    
    public void setActive(boolean active) {
        isActive = active;
    }
    
    /**
     * Retorna uma representação em string legível da âncora
     */
    @Override
    public String toString() {
        return String.format("NetworkAnchor{name='%s', type='%s', signal=%ddBm, bandwidth=%.2fMB, secured=%s}", 
            networkName, networkType, signalStrength, contributedBandwidth, secured);
    }
    
    /**
     * Verifica se esta âncora é a mesma que outra (baseado no ID da rede)
     */
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        
        NetworkAnchor that = (NetworkAnchor) obj;
        return networkId != null ? networkId.equals(that.networkId) : that.networkId == null;
    }
    
    @Override
    public int hashCode() {
        return networkId != null ? networkId.hashCode() : 0;
    }
    
    /**
     * Retorna o tempo desde que foi ancorado (em segundos)
     */
    public long getAnchorAgeSeconds() {
        if (anchoredAt == 0) return 0;
        return (System.currentTimeMillis() - anchoredAt) / 1000;
    }
    
    /**
     * Verifica se a âncora ainda é válida (não expirou)
     */
    public boolean isStillValid(long maxAgeSeconds) {
        return getAnchorAgeSeconds() <= maxAgeSeconds;
    }
    
    /**
     * Retorna a qualidade da conexão baseada na força do sinal
     */
    public String getConnectionQuality() {
        if (signalStrength > -50) {
            return "Excelente";
        } else if (signalStrength > -60) {
            return "Boa";
        } else if (signalStrength > -70) {
            return "Média";
        } else {
            return "Fraca";
        }
    }
    
    /**
     * Retorna um ícone emoji baseado no tipo de rede
     */
    public String getNetworkIcon() {
        switch (networkType) {
            case "WIFI":
                return "📶";
            case "CELLULAR":
                return "📱";
            case "BLUETOOTH":
                return "🔵";
            case "ETHERNET":
                return "🔌";
            default:
                return "🌐";
        }
    }
}
