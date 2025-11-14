from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver, Signal
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from datetime import timedelta
from .models import Product, Sale, ActivityLog


# This signal will fire when a product's stock becomes zero
stock_empty = Signal()

# PRE-SAVE SIGNAL - VALIDATE STOCK BEFORE CREATING A SALE
@receiver(pre_save, sender=Sale)
def validate_stock_before_sale(sender, instance, **kwargs):
    """
    Runs BEFORE a sale is created.
    Blocks the sale if requested quantity > available stock.
    Only runs for NEW sales (instance.pk is None).
    """
    if instance.pk is None:  # Only for create
        if instance.quantity > instance.product.stock:
            raise ValidationError("Not enough stock to complete this sale!")


 
# PRE-SAVE SIGNAL - DETECT SALE UPDATE & FIX STOCK
@receiver(pre_save, sender=Sale)
def adjust_stock_on_sale_update(sender, instance, **kwargs):
    """
    Detect sale updates and adjust stock accordingly.
    This runs only when existing sale is being updated.
    """
    if instance.pk:  # Sale exists → update
        old_sale = Sale.objects.get(pk=instance.pk)
        old_qty = old_sale.quantity
        new_qty = instance.quantity

        # If quantity increased → reduce stock
        if new_qty > old_qty:
            diff = new_qty - old_qty

            # Check if stock is enough
            if diff > instance.product.stock:
                raise ValidationError("Not enough stock for updating sale!")

            instance.product.stock -= diff
            instance.product.save()

        # If quantity decreased → restore stock
        elif new_qty < old_qty:
            diff = old_qty - new_qty
            instance.product.stock += diff
            instance.product.save()


 
# POST-SAVE SIGNAL - REDUCE STOCK FOR NEW SALES
@receiver(post_save, sender=Sale)
def reduce_stock_after_sale(sender, instance, created, **kwargs):
    """
    Runs AFTER a new sale is created, reduces product stock.
    Avoids running for updates (handled by pre_save).
    """
    if created:  # Only run on create
        product = instance.product
        product.stock -= instance.quantity
        product.save()

        # If stock becomes zero → trigger custom signal
        if product.stock == 0:
            stock_empty.send(sender=Product, product=product)

        # Log creation
        ActivityLog.objects.create(
            action="Sale Created",
            message=f"Sale #{instance.id} created  - {instance.quantity} units of {product.name}"
        )


 
# POST-SAVE SIGNAL  - LOG SALE UPDATE
@receiver(post_save, sender=Sale)
def log_sale_update(sender, instance, created, **kwargs):
    """
    Logs sale update events.
    """
    if not created:
        ActivityLog.objects.create(
            action="Sale Updated",
            message=f"Sale #{instance.id} updated."
        )


 
# PRE-DELETE SIGNAL  - BLOCK DELETION IF SALE IS TOO OLD
@receiver(pre_delete, sender=Sale)
def prevent_old_sale_deletion(sender, instance, **kwargs):
    """
    Prevent deleting sales older than 48 hours.
    """
    age = now() - instance.created_at
    if age > timedelta(hours=48):
        raise ValidationError("Cannot delete sales older than 48 hours!")


 
# POST-DELETE SIGNAL  - RESTORE STOCK ON DELETE
@receiver(post_delete, sender=Sale)
def restore_stock_after_delete(sender, instance, **kwargs):
    """
    After deleting a sale, restore product stock.
    """
    product = instance.product
    product.stock += instance.quantity
    product.save()

    # Log deletion
    ActivityLog.objects.create(
        action="Sale Deleted",
        message=f"Sale #{instance.id} deleted  - restored {instance.quantity} units to {product.name}"
    )

# CUSTOM SIGNAL RECEIVER  - STOCK EMPTY ALERT
@receiver(stock_empty)
def handle_zero_stock(sender, product, **kwargs):
    """
    Custom signal handler that runs when product stock becomes zero.
    """
    print(f"⚠ ALERT: Product '{product.name}' is now OUT OF STOCK!")

    ActivityLog.objects.create(
        action="Stock Empty",
        message=f"Product '{product.name}' just hit zero stock!"
    )
