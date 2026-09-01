package tn.esprit.smarttask.service.ai;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Primary;
import org.springframework.stereotype.Service;
import tn.esprit.smarttask.config.AIProperties;
import tn.esprit.smarttask.dto.ai.AIDriverRecommendationResponse;
import tn.esprit.smarttask.dto.response.AIRecommendationResponse;
import tn.esprit.smarttask.entity.Task;
import tn.esprit.smarttask.entity.User;
import tn.esprit.smarttask.exception.AIServiceUnavailableException;
import tn.esprit.smarttask.repository.TaskRepository;
import tn.esprit.smarttask.repository.UserRepository;
import tn.esprit.smarttask.service.AIService;

import java.util.Comparator;
import java.util.List;

@Service
@Primary
@RequiredArgsConstructor
@Slf4j
public class CompositeAIRecommendationService implements AIRecommendationService {

    private static final String ML_DISCLAIMER =
            "Recommendation powered by SmartTask AI microservice (explainable scoring / ML).";

    private final AIService aiService;
    private final AIProperties aiProperties;
    private final RuleBasedAIRecommendationService ruleBasedFallback;
    private final UserRepository userRepository;
    private final TaskRepository taskRepository;

    @Override
    public AIRecommendationResponse recommendDriver(Task task) {
        if (aiProperties.isEnabled()) {
            try {
                AIDriverRecommendationResponse ai = aiService.recommendDriver(task.getId());
                User driver = userRepository.findById(ai.getRecommendedDriverId()).orElse(null);
                String driverName = driver != null
                        ? driver.getFirstName() + " " + driver.getLastName()
                        : "Driver #" + ai.getRecommendedDriverId();
                return AIRecommendationResponse.builder()
                        .taskId(task.getId())
                        .recommendedDriverId(ai.getRecommendedDriverId())
                        .recommendedDriverName(driverName)
                        .scorePercent(ai.getScore() != null ? ai.getScore() : 0)
                        .reasons(ai.getReasons())
                        .ruleBased(false)
                        .disclaimer(ML_DISCLAIMER)
                        .build();
            } catch (AIServiceUnavailableException ex) {
                log.warn("AI service unavailable for task {}, using rule-based fallback", task.getId());
            }
        }
        return ruleBasedFallback.recommendDriver(task);
    }

    @Override
    public List<AIRecommendationResponse> getRecommendationsForManager() {
        List<AIRecommendationResponse> base = ruleBasedFallback.getRecommendationsForManager();
        if (!aiProperties.isEnabled()) {
            return base;
        }
        return base.stream()
                .map(rec -> taskRepository.findById(rec.getTaskId())
                        .map(this::recommendDriver)
                        .orElse(rec))
                .sorted(Comparator.comparingInt(AIRecommendationResponse::getScorePercent).reversed())
                .toList();
    }
}
