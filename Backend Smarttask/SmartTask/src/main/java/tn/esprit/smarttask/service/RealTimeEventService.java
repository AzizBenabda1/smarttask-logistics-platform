package tn.esprit.smarttask.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;
import tn.esprit.smarttask.dto.response.TaskLiveUpdate;
import tn.esprit.smarttask.entity.Task;

import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;

@Service
@Slf4j
public class RealTimeEventService {

    private static final ObjectMapper OBJECT_MAPPER = new ObjectMapper();
    private final Map<Long, CopyOnWriteArrayList<SseEmitter>> taskChannels = new ConcurrentHashMap<>();

    public SseEmitter subscribeTask(Long taskId) {
        SseEmitter emitter = new SseEmitter(3_600_000L);
        taskChannels.computeIfAbsent(taskId, id -> new CopyOnWriteArrayList<>()).add(emitter);

        emitter.onCompletion(() -> remove(taskId, emitter));
        emitter.onTimeout(() -> remove(taskId, emitter));
        emitter.onError(e -> remove(taskId, emitter));

        try {
            emitter.send(SseEmitter.event().name("connected").data("{\"status\":\"connected\"}"));
        } catch (IOException e) {
            remove(taskId, emitter);
        }
        return emitter;
    }

    public void publishTaskUpdate(Task task, String message) {
        TaskLiveUpdate update = TaskLiveUpdate.builder()
                .taskId(task.getId())
                .status(task.getStatus())
                .latitude(task.getLatitude())
                .longitude(task.getLongitude())
                .clientConfirmed(task.isClientConfirmed())
                .hasProofOfDelivery(task.getProofOfDeliveryImage() != null && !task.getProofOfDeliveryImage().isBlank())
                .message(message)
                .timestamp(System.currentTimeMillis())
                .build();
        publish(task.getId(), update);
    }

    private void publish(Long taskId, TaskLiveUpdate update) {
        List<SseEmitter> emitters = taskChannels.get(taskId);
        if (emitters == null || emitters.isEmpty()) return;

        for (SseEmitter emitter : emitters) {
            try {
                emitter.send(SseEmitter.event().name("update").data(OBJECT_MAPPER.writeValueAsString(update)));
            } catch (IOException ex) {
                remove(taskId, emitter);
            }
        }
    }

    private void remove(Long taskId, SseEmitter emitter) {
        CopyOnWriteArrayList<SseEmitter> list = taskChannels.get(taskId);
        if (list != null) {
            list.remove(emitter);
            if (list.isEmpty()) taskChannels.remove(taskId);
        }
        emitter.complete();
    }
}
