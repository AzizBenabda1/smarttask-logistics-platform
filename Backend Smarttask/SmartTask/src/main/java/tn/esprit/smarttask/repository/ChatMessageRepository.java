package tn.esprit.smarttask.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import tn.esprit.smarttask.entity.ChatMessage;

import java.util.List;

@Repository
public interface ChatMessageRepository extends JpaRepository<ChatMessage, Long> {

    List<ChatMessage> findTop30ByUserIdAndSessionIdOrderByCreatedAtAsc(Long userId, String sessionId);

    List<ChatMessage> findTop30ByUserIdOrderByCreatedAtDesc(Long userId);
}
