export type OrderStatus = 'PENDING' | 'VERIFIED' | 'PREPARING' | 'READY' | 'IN_DELIVERY' | 'DELIVERED' | 'RECEIVED' | 'CANCELLED';
export type IncidentType = string;
export type IncidentStatus = 'OPEN' | 'IN_PROGRESS' | 'RESOLVED' | 'CLOSED';

export interface Order {
  id: number;
  clientId: number;
  clientName?: string;
  clientPhone?: string;
  productTypeId?: number;
  productTypeName?: string;
  productTypeCode?: string;
  products: string;
  quantity: number;
  amount: number;
  phone?: string;
  deliveryAddress: string;
  scheduledDate?: string;
  scheduledTime?: string;
  instructions?: string;
  priority: string;
  status: OrderStatus;
  taskId?: number;
  taskStatus?: string;
  clientConfirmed?: boolean;
  createdAt?: string;
}

export interface OrderRequest {
  /** Required when operator updates; omitted when client creates own order */
  clientId?: number;
  productTypeId?: number;
  customProductType?: string;
  products?: string;
  quantity: number;
  amount: number;
  phone?: string;
  deliveryAddress: string;
  scheduledDate?: string;
  scheduledTime?: string;
  instructions?: string;
  priority: string;
}

export interface OperatorDashboard {
  ordersToday: number;
  pendingOrders: number;
  verifiedOrders: number;
  readyOrders: number;
  tasksToPrepare: number;
  tasksInProgress: number;
  tasksCompleted: number;
  openIncidents: number;
  deliveriesInProgress: number;
  alerts: NotificationItem[];
}

export interface DriverDashboard {
  missionsToday: number;
  toAccept: number;
  accepted: number;
  inProgress: number;
  completed: number;
  delayed: number;
  notifications: NotificationItem[];
}

export interface ClientDashboard {
  activeOrders: number;
  deliveredOrders: number;
  upcomingDeliveries: number;
  lastOrder?: Order;
  notifications: NotificationItem[];
}

export interface Incident {
  id: number;
  type: IncidentType;
  description: string;
  priority: string;
  status: IncidentStatus;
  taskId?: number;
  orderId?: number;
  reporterName?: string;
  createdAt: string;
}

export interface IncidentRequest {
  taskId?: number;
  orderId?: number;
  type: string;
  description: string;
  priority: string;
}

export interface Review {
  id: number;
  taskId: number;
  rating: number;
  comment?: string;
  createdAt: string;
}

export interface ReviewRequest {
  taskId: number;
  rating: number;
  comment?: string;
}

export interface DeliveryTracking {
  taskId: number;
  orderId?: number;
  currentStatus: string;
  driverName?: string;
  deliveryAddress: string;
  estimatedArrival?: string;
  deadline?: string;
  clientConfirmed: boolean;
  hasProofOfDelivery?: boolean;
  latitude?: number;
  longitude?: number;
  timeline: TimelineStep[];
}

export interface TaskLiveUpdate {
  taskId: number;
  status: string;
  latitude?: number;
  longitude?: number;
  clientConfirmed: boolean;
  hasProofOfDelivery: boolean;
  message?: string;
  timestamp: number;
}

export interface TimelineStep {
  label: string;
  completed: boolean;
  current: boolean;
}

export interface DriverPerformance {
  totalDeliveries: number;
  onTimeDeliveries: number;
  delayedDeliveries: number;
  successRate: number;
  averageMinutes: number;
  incidents: number;
}

export interface DriverRouteStop {
  order: number;
  taskId: number;
  title: string;
  zone?: string;
  deliveryAddress: string;
  priority: string;
  estimatedMinutes: number;
  urgencyLabel: string;
}

export interface DriverRouteOptimization {
  driverId: number;
  stops: DriverRouteStop[];
  manualTotalMinutes: number;
  optimizedTotalMinutes: number;
  estimatedTimeSavedMinutes: number;
  aiPowered: boolean;
  summary: string;
}

export interface NotificationItem {
  id: number;
  type: string;
  title: string;
  message: string;
  priority: string;
  read: boolean;
  relatedTaskId?: number;
  createdAt: string;
}

export interface Task {
  id: number;
  title: string;
  description?: string;
  clientId: number;
  clientName?: string;
  clientPhone?: string;
  driverId?: number;
  driverName?: string;
  deliveryAddress: string;
  zone?: string;
  scheduledDate?: string;
  scheduledTime?: string;
  deadline: string;
  priority: string;
  status: string;
  products?: string;
  instructions?: string;
  delayed: boolean;
  orderId?: number;
  clientConfirmed?: boolean;
  hasProofOfDelivery?: boolean;
  deliveredAt?: string;
}
