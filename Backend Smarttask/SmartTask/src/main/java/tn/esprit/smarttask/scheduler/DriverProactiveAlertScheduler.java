package tn.esprit.smarttask.scheduler;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import tn.esprit.smarttask.config.DriverAlertProperties;
import tn.esprit.smarttask.service.driver.DriverProactiveAlertService;

@Component
@RequiredArgsConstructor
@Slf4j
public class DriverProactiveAlertScheduler {

    private final DriverProactiveAlertService alertService;
    private final DriverAlertProperties properties;

    @Scheduled(fixedDelayString = "${app.driver.alerts.interval-ms:300000}")
    public void runDriverAlerts() {
        if (!properties.isEnabled()) return;
        try {
            alertService.scanAndNotify();
        } catch (Exception ex) {
            log.error("Driver proactive alert scan failed: {}", ex.getMessage());
        }
    }
}
