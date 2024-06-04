class CustomerService:
    ORDER_STATUS = "Order Status"
    SHIPPING_AND_DELIVERY = "Shipping and Delivery"
    RETURNS_AND_REFUNDS = "Returns and Refunds"
    PAYMENT_ISSUES = "Payment Issues"
    ACCOUNT_ISSUES = "Account Issues"
    PRODUCT_INQUIRY = "Product Inquiry"
    TECHNICAL_SUPPORT = "Technical Support"
    FEEDBACK_AND_SUGGESTIONS = "Feedback and Suggestions"
    REPORT_A_PROBLEM = "Report a Problem"
    GENERAL_INQUIRY = "General Inquiry"

    TOPIC_CHOICES = [
        (ORDER_STATUS, ORDER_STATUS),
        (SHIPPING_AND_DELIVERY, SHIPPING_AND_DELIVERY),
        (RETURNS_AND_REFUNDS, RETURNS_AND_REFUNDS),
        (PAYMENT_ISSUES, PAYMENT_ISSUES),
        (ACCOUNT_ISSUES, ACCOUNT_ISSUES),
        (PRODUCT_INQUIRY, PRODUCT_INQUIRY),
        (TECHNICAL_SUPPORT, TECHNICAL_SUPPORT),
        (FEEDBACK_AND_SUGGESTIONS, FEEDBACK_AND_SUGGESTIONS),
        (REPORT_A_PROBLEM, REPORT_A_PROBLEM),
        (GENERAL_INQUIRY, GENERAL_INQUIRY)
    ]
