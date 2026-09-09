package tn.esprit.smarttask.event;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;
import org.springframework.transaction.event.TransactionPhase;
import org.springframework.transaction.event.TransactionalEventListener;
import tn.esprit.smarttask.entity.Priority;
import tn.esprit.smarttask.service.automation.ExpressDeliveryAutomationService;

@Component
@RequiredArgsConstructor
@Slf4j
public class AutomationEventListener {

    private final ExpressDeliveryAutomationService expressChain;

    @Async
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void onOrderVerified(OrderVerifiedEvent event) {
        try {
            Priority priority = Priority.valueOf(event.getPriority());
            if (expressChain.shouldAutoTrigger(priority)) {
                log.info("Express Autonomous chain for order #{} (after operator validation)", event.getOrderId());
                expressChain.execute(event.getOrderId());
            }
        } catch (Exception ex) {
            log.error("Express automation failed for order #{}: {}", event.getOrderId(), ex.getMessage());
        }
    }
}
