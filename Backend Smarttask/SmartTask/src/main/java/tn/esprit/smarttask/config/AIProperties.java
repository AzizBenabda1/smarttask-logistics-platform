package tn.esprit.smarttask.config;

import lombok.Getter;
import lombok.Setter;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

@Configuration
@ConfigurationProperties(prefix = "app.ai")
@Getter
@Setter
public class AIProperties {
    private boolean enabled = true;
    private String serviceUrl = "http://localhost:8000";
    private int timeoutSeconds = 10;
}
