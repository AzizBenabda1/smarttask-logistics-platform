package tn.esprit.smarttask.service.ai;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import tn.esprit.smarttask.dto.response.AIRecommendationResponse;
import tn.esprit.smarttask.entity.*;
import tn.esprit.smarttask.repository.DriverProfileRepository;
import tn.esprit.smarttask.repository.TaskRepository;
import tn.esprit.smarttask.repository.UserRepository;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

@Service
@RequiredArgsConstructor
public class RuleBasedAIRecommendationService implements AIRecommendationService {

    private static final String DISCLAIMER = "Recommendations are rule-based (not ML). Connect an AI service later via AIRecommendationService.";

    private final UserRepository userRepository;
    private final DriverProfileRepository driverProfileRepository;
    private final TaskRepository taskRepository;

    @Override
    public AIRecommendationResponse recommendDriver(Task task) {
        List<User> drivers = userRepository.findByRole(Role.DRIVER);
        User best = null;
        int bestScore = 0;
        List<String> bestReasons = List.of();

        for (User driver : drivers) {
            if (!driver.isActive()) continue;
            DriverProfile profile = driverProfileRepository.findByUserId(driver.getId()).orElse(null);
            int score = 0;
            List<String> reasons = new ArrayList<>();

            if (profile != null && profile.getStatus() == DriverStatus.AVAILABLE) {
                score += 40;
                reasons.add("Available");
            }
            if (profile != null && task.getZone() != null && task.getZone().equalsIgnoreCase(profile.getZone())) {
                score += 25;
                reasons.add("Knows the zone");
            }
            if (profile != null && profile.getCurrentLoad() < 3) {
                score += 20;
                reasons.add("Low current load");
            }
            if (profile != null && profile.getPerformanceScore().doubleValue() >= 75) {
                score += 15;
                reasons.add("Good performance history");
            }

            if (score > bestScore) {
                bestScore = score;
                best = driver;
                bestReasons = reasons;
            }
        }

        if (best == null) {
            return AIRecommendationResponse.builder()
                    .taskId(task.getId())
                    .scorePercent(0)
                    .reasons(List.of("No available driver found"))
                    .ruleBased(true)
                    .disclaimer(DISCLAIMER)
                    .build();
        }

        return AIRecommendationResponse.builder()
                .taskId(task.getId())
                .recommendedDriverId(best.getId())
                .recommendedDriverName(best.getFirstName() + " " + best.getLastName())
                .scorePercent(Math.min(bestScore, 100))
                .reasons(bestReasons)
                .ruleBased(true)
                .disclaimer(DISCLAIMER)
                .build();
    }

    @Override
    public List<AIRecommendationResponse> getRecommendationsForManager() {
        return taskRepository.findByDriverIsNullAndStatus(TaskStatus.PENDING).stream()
                .sorted(Comparator.comparing(Task::getDeadline))
                .limit(5)
                .map(this::recommendDriver)
                .toList();
    }
}
