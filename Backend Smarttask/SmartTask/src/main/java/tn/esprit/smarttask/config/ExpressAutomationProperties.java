package tn.esprit.smarttask.config;

import lombok.Getter;
import lombok.Setter;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

@Configuration
@ConfigurationProperties(prefix = "app.automation.express")
@Getter
@Setter
public class ExpressAutomationProperties {

    /** Active la chaîne Livraison Express Autonome à la création de commande */
    private boolean enabled = true;

    /** Score IA minimum (0-100) pour assigner automatiquement un chauffeur */
    private int minDriverScore = 70;

    /** Priorités déclenchant l'automation auto (HIGH, CRITICAL) */
    private String autoTriggerPriorities = "HIGH,CRITICAL";
}
