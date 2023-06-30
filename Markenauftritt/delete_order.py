from googleads import ad_manager


def main(client, order_id) :
    order_service = client.GetService('OrderService', version="v202211")

  # Create statement object to select a single order by an ID.
    statement = (ad_manager.StatementBuilder(version='v202211')
               .Where('id = :orderId')
               .WithBindVariable('orderId', int(order_id)))

    # Get orders by statement.
    response = order_service.performOrderAction({'xsi_type':'DeleteOrders'},statement.ToStatement())
    print("Deleted order with the id: ", order_id )

