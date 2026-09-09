package tn.esprit.smarttask.repository;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.stereotype.Repository;
import tn.esprit.smarttask.entity.Order;
import tn.esprit.smarttask.entity.OrderStatus;

import java.time.LocalDate;
import java.util.List;

@Repository
public interface OrderRepository extends JpaRepository<Order, Long>, JpaSpecificationExecutor<Order> {
    List<Order> findByClientIdOrderByCreatedAtDesc(Long clientId);
    List<Order> findByStatusOrderByCreatedAtDesc(OrderStatus status);
    List<Order> findByScheduledDate(LocalDate date);
    long countByStatus(OrderStatus status);
    long countByClient_Id(Long clientId);
    Page<Order> findByClientIdOrderByCreatedAtDesc(Long clientId, Pageable pageable);
    List<Order> findByStatusAndTaskIdIsNullOrderByCreatedAtDesc(OrderStatus status);
}
