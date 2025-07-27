package com.comunicador;

import java.util.ArrayList;
import java.util.List;

public class BandwidthAccumulator {
    
    private double targetBandwidthMB;
    private double currentBandwidthMB;
    private List<NetworkAnchor> anchoredNetworks;
    
    public BandwidthAccumulator(double targetBandwidthMB) {
        this.targetBandwidthMB = targetBandwidthMB;
        this.currentBandwidthMB = 0.0;
        this.anchoredNetworks = new ArrayList<>();
    }
    
    public void addBandwidth(double additionalBandwidthMB, NetworkAnchor networkAnchor) {
        this.currentBandwidthMB += additionalBandwidthMB;
        anchoredNetworks.add(networkAnchor);
    }
    
    public boolean hasEnoughBandwidth() {
        return currentBandwidthMB >= targetBandwidthMB;
    }
    
    public double getCurrentBandwidth() {
        return currentBandwidthMB;
    }
    
    public List<NetworkAnchor> getAnchoredNetworks() {
        return new ArrayList<>(anchoredNetworks);
    }
    
    public void reset() {
        this.currentBandwidthMB = 0.0;
        this.anchoredNetworks.clear();
    }
}
