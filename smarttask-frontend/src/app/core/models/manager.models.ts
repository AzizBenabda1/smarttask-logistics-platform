export type TaskStatus = 'PENDING' | 'ASSIGNED' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED' | 'DELAYED';
export type Priority = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
export type DriverStatus = 'AVAILABLE' | 'BUSY' | 'OFFLINE';
export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export interface ChartPoint {
  label: string;
  value: number;
}

export interface PageResponse<T> {
  content: T[];
  page: number;
  size: number;
  totalElements: number;
  totalPages: number;
  first: boolean;
  last: boolean;
}

export type IncidentStatus = 'OPEN' | 'IN_PROGRESS' | 'RESOLVED' | 'CLOSED';

export interface IncidentItem {
  id: number;
  type: string;
  description: string;
  priority: Priority;
  status: IncidentStatus;
  taskId?: number;
  orderId?: number;
  reporterName?: string;
  createdAt?: string;
}

export interface ManagerDashboard {
  totalTasks: number;
  pendingTasks: number;
  inProgressTasks: number;
  completedTasks: number;
  delayedTasks: number;
  deliveriesToday: number;
  availableDrivers: number;
  busyDrivers: number;
  totalDrivers: number;
  totalOperators: number;
  totalClients: number;
  aiRecommendations: AIRecommendation[];
  alerts: NotificationItem[];
  tasksByStatus: ChartPoint[];
  onTimeRate: number;
  delayRate: number;
}

export interface Task {
  id: number;
  title: string;
  description?: string;
  clientId: number;
  clientName?: string;
  driverId?: number;
  driverName?: string;
  deliveryAddress: string;
  zone?: string;
  scheduledDate?: string;
  scheduledTime?: string;
  deadline: string;
  priority: Priority;
  status: TaskStatus;
  deliveryType?: string;
  weightQuantity?: string;
  instructions?: string;
  estimatedMinutes?: number;
  actualMinutes?: number;
  createdAt?: string;
  updatedAt?: string;
  delayed: boolean;
  latitude?: number;
  longitude?: number;
}

export interface TaskRequest {
  title: string;
  description?: string;
  clientId: number;
  driverId?: number;
  deliveryAddress: string;
  zone?: string;
  scheduledDate?: string;
  scheduledTime?: string;
  deadline: string;
  priority: Priority;
  deliveryType?: string;
  weightQuantity?: string;
  instructions?: string;
  estimatedMinutes?: number;
}

export interface TaskHistory {
  id: number;
  action: string;
  oldStatus?: TaskStatus;
  newStatus?: TaskStatus;
  performedByName?: string;
  createdAt: string;
}

export interface Driver {
  id: number;
  firstName: string;
  lastName: string;
  email: string;
  phone?: string;
  status: DriverStatus;
  zone?: string;
  currentLoad: number;
  totalDeliveries: number;
  performanceScore: number;
  activeTasks: number;
}

export interface Client {
  id: number;
  firstName: string;
  lastName: string;
  email: string;
  phone?: string;
  totalTasks: number;
  activeTasks: number;
}

export interface Operator {
  id: number;
  firstName: string;
  lastName: string;
  email: string;
  phone?: string;
  active: boolean;
}

export interface DelayedTask {
  taskId: number;
  title: string;
  driverName?: string;
  deadline: string;
  delayMinutes: number;
  riskLevel: RiskLevel;
  status: TaskStatus;
  priority: Priority;
}

export interface NotificationItem {
  id: number;
  type: string;
  title: string;
  message: string;
  priority: Priority;
  read: boolean;
  relatedTaskId?: number;
  createdAt: string;
}

export interface Analytics {
  totalDeliveries: number;
  completedDeliveries: number;
  onTimeDeliveries: number;
  delayedDeliveries: number;
  averageDeliveryMinutes: number;
  incidents: number;
  averagePerformance: number;
  deliveriesByDay: ChartPoint[];
  deliveriesByStatus: ChartPoint[];
  delaysByDay: ChartPoint[];
  tasksByPriority: ChartPoint[];
}

export interface AIRecommendation {
  taskId: number;
  recommendedDriverId: number;
  recommendedDriverName: string;
  scorePercent: number;
  reasons: string[];
  ruleBased: boolean;
  disclaimer: string;
}
