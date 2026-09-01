package tn.esprit.smarttask.service.ai;

import tn.esprit.smarttask.dto.response.AIRecommendationResponse;
import tn.esprit.smarttask.entity.Task;

import java.util.List;

public interface AIRecommendationService {
    AIRecommendationResponse recommendDriver(Task task);
    List<AIRecommendationResponse> getRecommendationsForManager();
}
