package tn.esprit.smarttask.config;

import lombok.Getter;
import lombok.Setter;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

@Configuration
@ConfigurationProperties(prefix = "app.driver.alerts")
@Getter
@Setter
public class DriverAlertProperties {

    private boolean enabled = true;

    /** Intervalle entre deux scans (ms) — défaut 5 min */
    private long intervalMs = 300_000L;

    /** Alerte si deadline dans N minutes */
    private int deadlineWarningMinutes = 45;

    /** Alerte risque retard si deadline dans N minutes */
    private int delayRiskMinutes = 20;

    /** Ne pas renvoyer la même alerte avant N minutes */
    private int dedupMinutes = 30;
}
