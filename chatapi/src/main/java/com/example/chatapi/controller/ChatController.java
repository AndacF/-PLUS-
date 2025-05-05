package com.example.chatapi.controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.http.*;
import org.springframework.web.client.RestTemplate;
import com.fasterxml.jackson.annotation.JsonProperty;

@RestController
public class ChatController {

    @PostMapping("/chat")
    public ResponseEntity<String> chat(@RequestBody Request request) {
        // Python servisine istek atmak için RestTemplate
        RestTemplate restTemplate = new RestTemplate();
        String pythonServiceUrl = "http://localhost:5000/generate";

        // İsteği Python servisine gönder
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<Request> entity = new HttpEntity<>(request, headers);
        ResponseEntity<String> response = restTemplate.postForEntity(pythonServiceUrl, entity, String.class);

        // Python servisinden gelen yanıtı döndür
        return ResponseEntity.ok(response.getBody());
    }
}

// Request
class Request {
    @JsonProperty("isim")
    private String isim;

    @JsonProperty("ateş")
    private String ates;

    @JsonProperty("nabız")
    private String nabiz;

    @JsonProperty("tansiyon")
    private String tansiyon;

    @JsonProperty("not")
    private String not;

    // Getters ve Setters
    public String getIsim() { return isim; }
    public void setIsim(String isim) { this.isim = isim; }
    public String getAtes() { return ates; }
    public void setAtes(String ates) { this.ates = ates; }
    public String getNabiz() { return nabiz; }
    public void setNabiz(String nabiz) { this.nabiz = nabiz; }
    public String getTansiyon() { return tansiyon; }
    public void setTansiyon(String tansiyon) { this.tansiyon = tansiyon; }
    public String getNot() { return not; }
    public void setNot(String not) { this.not = not; }
}