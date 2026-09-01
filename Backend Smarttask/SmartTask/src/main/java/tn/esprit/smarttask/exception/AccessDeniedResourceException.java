package tn.esprit.smarttask.exception;

public class AccessDeniedResourceException extends RuntimeException {
    public AccessDeniedResourceException(String message) {
        super(message);
    }
}
