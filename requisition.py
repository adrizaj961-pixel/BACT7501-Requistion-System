from decimal import Decimal

class Requisition:

    next_id=10001

    def __init__(self, date, staff_id, staff_name):

        self.date=date
        self.staff_id=staff_id
        self.staff_name=staff_name

        self.requisition_id=Requisition.next_id
        Requisition.next_id +=1

        self.items=[]
        self.total=Decimal("0.00")
        self.status="Pending"
        self.approval_reference=None

    def add_requisition(self, items):

        if not items:
            raise ValueError("At least one item is required.")
        
        total=Decimal("0.00")
        checked_items=[]

        for item in items:
            name=item["name"].strip()
            price=Decimal(str(item["price"]))

            if not name or not price.is_finite() or price<=0:
                raise ValueError("Invalid item name or price.")

            checked_items.append({
                "name": name,
                "price": price
            })
            total+=price

        self.items=checked_items
        self.total=total

        return self.total
    
    
    def approve_requisition(self):

        if not self.items:
            raise ValueError("Add items before approval.")

        if self.total < Decimal("500.00"):
            self.status="Approved"

            self.approval_reference=(
                f"{self.staff_id}{str(self.requisition_id)[-3:]}"
            )

        else:
            self.status="Pending"
            self.approval_reference=None

        return self.status

    def respond_requisition(self, decision):

        if decision not in ("Approved", "Not approved"):
            raise ValueError("Invalid manager decision.")

        if self.status !="Pending":
            raise ValueError(
                "Only pending requisitions can be changed."
            )

        if decision=="Approved":
            self.status="Approved"

            self.approval_reference=(
                f"{self.staff_id}{str(self.requisition_id)[-3:]}"
            )

        else:
            self.status="Not approved"
            self.approval_reference=None

        return self.status

    @staticmethod
    def requisition_statistics(requisitions):

        total = len(requisitions)
        approved=0
        pending=0
        not_approved=0

        for request in requisitions:

            if request.status=="Approved":
                approved += 1

            elif request.status=="Pending":
                pending += 1

            elif request.status=="Not approved":
                not_approved +=1

        return {
            "total": total,
            "approved": approved,
            "pending": pending,
            "not_approved": not_approved
        }

    @staticmethod
    def display_requisitions(requisitions):

        print("\n----- All Requisitions -----")

        for request in requisitions:

            print("Date:", request.date)
            print("Requisition ID:", request.requisition_id)
            print("Staff ID:", request.staff_id)
            print("Staff Name:", request.staff_name)
            print(f"Total: ${request.total:.2f}")
            print("Status:", request.status)

            if request.approval_reference is None:
                print("Approval Reference Number: Not available")
            else:
                print("Approval Reference Number:",
                      request.approval_reference)

            print("------------------------------")