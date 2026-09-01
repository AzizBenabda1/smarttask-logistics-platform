package tn.esprit.smarttask.event;

import lombok.Getter;
import org.springframework.context.ApplicationEvent;

@Getter
public class OrderCreatedEvent extends ApplicationEvent {

    private final Long orderId;
    private final String priority;

    public OrderCreatedEvent(Object source, Long orderId, String priority) {
        super(source);
        this.orderId = orderId;
        this.priority = priority;
    }
}
