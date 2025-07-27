package com.comunicador;

import java.util.ArrayList;
import java.util.List;

public class MessageQueue {
    
    private List<PendingMessage> messages;
    
    public MessageQueue() {
        this.messages = new ArrayList<>();
        
        // Adiciona mensagem padrão para teste
        messages.add(new PendingMessage(
            "teste@example.com",
            "Mensagem enviada via Network Sniffer",
            "Esta mensagem foi enviada usando o sistema de ancoragem superficial de redes!",
            System.currentTimeMillis()
        ));
    }
    
    public void addMessage(PendingMessage message) {
        messages.add(message);
    }
    
    public List<PendingMessage> getAllMessages() {
        return new ArrayList<>(messages);
    }
    
    public void clearMessages() {
        messages.clear();
    }
    
    public static class PendingMessage {
        private String destination;
        private String subject;
        private String content;
        private long timestamp;
        
        public PendingMessage(String destination, String subject, String content, long timestamp) {
            this.destination = destination;
            this.subject = subject;
            this.content = content;
            this.timestamp = timestamp;
        }
        
        public String getDestination() { return destination; }
        public String getSubject() { return subject; }
        public String getContent() { return content; }
        public long getTimestamp() { return timestamp; }
    }
}
