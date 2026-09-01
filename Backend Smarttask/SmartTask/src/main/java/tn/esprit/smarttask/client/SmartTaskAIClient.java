package tn.esprit.smarttask.client;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;
import tn.esprit.smarttask.config.AIProperties;
import tn.esprit.smarttask.dto.ai.*;
import tn.esprit.smarttask.exception.AIServiceUnavailableException;

import java.time.Duration;
import java.util.Map;

@Component
@RequiredArgsConstructor
@Slf4j
public class SmartTaskAIClient {

    private final WebClient smartTaskAIWebClient;
    private final AIProperties aiProperties;

    public Map<String, Object> health() {
        return get("/api/ai/health", new ParameterizedTypeReference<>() {});
    }

    public Map<String, Object> modelStatus() {
        return get("/api/ai/model/status", new ParameterizedTypeReference<>() {});
    }

    public AIDelayPredictionResponse predictDelay(AIDelayPredictionRequest request) {
        return post("/api/ai/predict/delay", request, AIDelayPredictionResponse.class);
    }

    public AIDeliveryTimePredictionResponse predictDeliveryTime(AIDeliveryTimePredictionRequest request) {
        return post("/api/ai/predict/delivery-time", request, AIDeliveryTimePredictionResponse.class);
    }

    public AIDriverRecommendationResponse recommendDriver(AIDriverRecommendationRequest request) {
        return post("/api/ai/recommend/driver", request, AIDriverRecommendationResponse.class);
    }

    public AITaskPrioritizationResponse prioritizeTask(AITaskPrioritizationRequest request) {
        return post("/api/ai/prioritize/task", request, AITaskPrioritizationResponse.class);
    }

    public AIAnomalyDetectionResponse detectAnomaly(Map<String, Object> request) {
        return post("/api/ai/detect/anomaly", request, AIAnomalyDetectionResponse.class);
    }

    public AIChatResponse chat(AIChatRequest request) {
        return post("/api/ai/chat", request, AIChatResponse.class);
    }

    public AIChatSuggestionsResponse chatSuggestions(String role) {
        return get("/api/ai/chat/suggestions?role=" + role, new ParameterizedTypeReference<>() {});
    }

    public AIRouteOptimizationResponse optimizeRoute(AIRouteOptimizationRequest request) {
        return post("/api/ai/optimize/route", request, AIRouteOptimizationResponse.class);
    }

    public AIDeliverySuccessPredictionResponse predictDeliverySuccess(
            AIDeliverySuccessPredictionRequest request) {
        return post("/api/ai/predict/delivery-success", request, AIDeliverySuccessPredictionResponse.class);
    }

    private <T> T get(String path, ParameterizedTypeReference<T> type) {
        ensureEnabled();
        try {
            return smartTaskAIWebClient.get()
                    .uri(path)
                    .retrieve()
                    .bodyToMono(type)
                    .timeout(Duration.ofSeconds(aiProperties.getTimeoutSeconds()))
                    .onErrorMap(this::mapError)
                    .block();
        } catch (Exception ex) {
            throw mapRuntime(ex);
        }
    }

    private <T> T post(String path, Object body, Class<T> responseType) {
        ensureEnabled();
        try {
            return smartTaskAIWebClient.post()
                    .uri(path)
                    .contentType(MediaType.APPLICATION_JSON)
                    .bodyValue(body)
                    .retrieve()
                    .bodyToMono(responseType)
                    .timeout(Duration.ofSeconds(aiProperties.getTimeoutSeconds()))
                    .onErrorMap(this::mapError)
                    .block();
        } catch (Exception ex) {
            throw mapRuntime(ex);
        }
    }

    private void ensureEnabled() {
        if (!aiProperties.isEnabled()) {
            throw new AIServiceUnavailableException("SmartTask AI service is disabled");
        }
    }

    private Throwable mapError(Throwable ex) {
        if (ex instanceof WebClientResponseException wex) {
            log.warn("AI service HTTP {}: {}", wex.getStatusCode(), wex.getResponseBodyAsString());
            return new AIServiceUnavailableException("AI service error: " + wex.getStatusCode(), wex);
        }
        return ex;
    }

    private AIServiceUnavailableException mapRuntime(Exception ex) {
        if (ex instanceof AIServiceUnavailableException aiEx) {
            return aiEx;
        }
        log.error("AI service call failed: {}", ex.getMessage());
        return new AIServiceUnavailableException("SmartTask AI service is unavailable", ex);
    }
}
