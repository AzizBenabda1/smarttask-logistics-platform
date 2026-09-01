package tn.esprit.smarttask.config;

import io.netty.channel.ChannelOption;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.netty.http.client.HttpClient;

import java.time.Duration;

@Configuration
public class AIClientConfig {

    @Bean
    public WebClient smartTaskAIWebClient(AIProperties properties) {
        HttpClient httpClient = HttpClient.create()
                .responseTimeout(Duration.ofSeconds(properties.getTimeoutSeconds()))
                .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, properties.getTimeoutSeconds() * 1000);

        return WebClient.builder()
                .baseUrl(properties.getServiceUrl())
                .clientConnector(new ReactorClientHttpConnector(httpClient))
                .build();
    }
}
