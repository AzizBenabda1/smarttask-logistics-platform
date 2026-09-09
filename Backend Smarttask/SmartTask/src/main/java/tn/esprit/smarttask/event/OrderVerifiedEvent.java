package tn.esprit.smarttask.event;

import lombok.Getter;
import org.springframework.context.ApplicationEvent;

@Getter
public class OrderVerifiedEvent extends ApplicationEvent {

    private final Long orderId;
    private final String priority;

    public OrderVerifiedEvent(Object source, Long orderId, String priority) {
        super(source);
        this.orderId = orderId;
        this.priority = priority;
    }
}
