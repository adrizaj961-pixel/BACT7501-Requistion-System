import sys
from decimal import Decimal, InvalidOperation

from PySide6.QtWidgets import (
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QLineEdit,
    QDateEdit,
    QFormLayout,
    QPushButton,
    QMessageBox
)

from PySide6.QtCore import QDate, Qt
from requisition import Requisition

app=QApplication(sys.argv)

window=QWidget()
window.setWindowTitle("Purchase Requisition System")
window.resize(1000, 600)

# Create a vertical layout
layout=QVBoxLayout()

# Create the main heading
heading=QLabel("Purchase Requisition System")

# Make the heading larger
heading.setStyleSheet("font-size: 26px; font-weight: bold;")

# Add the heading to the layout
layout.addWidget(heading)
layout.setAlignment(heading, Qt.AlignTop)

# Create a form for staff information
staff_form=QFormLayout()

# Staff name input
staff_name_input=QLineEdit()
staff_name_input.setPlaceholderText("Enter staff name")

# Staff ID input
staff_id_input=QLineEdit()
staff_id_input.setPlaceholderText("Example: FN19")

# Date input
date_input=QDateEdit()
date_input.setCalendarPopup(True)
date_input.setDate(QDate.currentDate())
date_input.setDisplayFormat("dd/MM/yyyy")

# Add input fields to the form
staff_form.addRow("Staff Name:", staff_name_input)
staff_form.addRow("Staff ID:", staff_id_input)
staff_form.addRow("Date:", date_input)

# Add the form to the main layout
layout.addLayout(staff_form)

# Create the purchase item form
item_form=QFormLayout()

# Input for item name
item_name_input=QLineEdit()
item_name_input.setPlaceholderText("Example: Keyboard")

# Input for item price
item_price_input=QLineEdit()
item_price_input.setPlaceholderText("Example: 150.00")

# Add both fields to the form
item_form.addRow("Item Name:", item_name_input)
item_form.addRow("Item Price ($):", item_price_input)

# Add the item form to the main window
layout.addLayout(item_form)

# Store purchase items in a list
items=[]
requisitions=[]

# Label for displaying the total
items_label=QLabel("Items: 0 | Total: $0.00")

# Create the Add Item button
add_button=QPushButton("Add Item")

# Add the button and label to the window
layout.addWidget(add_button)
layout.addWidget(items_label)

# Function to add an item
def add_item():
    print("Add Item clicked")
    name=item_name_input.text().strip()

    try:
        price=Decimal(item_price_input.text().strip())
    except InvalidOperation:
        QMessageBox.warning(
            window, "Invalid Price", "Enter a valid number."
        )
        return

    if not name or not price.is_finite() or price <= 0:
        QMessageBox.warning(
            window, "Invalid Item",
            "Enter an item name and a positive price."
        )
        return

    items.append({"name": name, "price": str(price)})

    total=sum(
        (Decimal(item["price"]) for item in items),
        Decimal("0.00")
    )

    items_label.setText(
        f"Items: {len(items)} | Total: ${total:.2f}"
    )

    item_name_input.clear()
    item_price_input.clear()

#Connect the add Item button to the function
add_button.clicked.connect(add_item)

# Create the Submit Requisition button
submit_button = QPushButton("Submit Requisition")

# Add the button to the window
layout.addWidget(submit_button)

# Create a table to display all requisitions
table=QTableWidget()

# Set the number of columns
table.setColumnCount(7)

# Give names to the columns
table.setHorizontalHeaderLabels([
    "Date",
    "Requisition ID",
    "Staff ID",
    "Staff Name",
    "Total",
    "Status",
    "Approval Reference"
])

# Add the table to the window
layout.addWidget(table)

# Display requisition statistics
stats_label=QLabel(
    "Submitted: 0 | Approved: 0 | Pending: 0 | Not Approved: 0"
)

stats_label.setStyleSheet(
    "font-size: 15px; font-weight: bold;"
)

layout.addWidget(stats_label)

# Update the statistics displayed in the GUI
def update_statistics():

    stats=Requisition.requisition_statistics(requisitions)

    stats_label.setText(
        f"Submitted: {stats['total']} | "
        f"Approved: {stats['approved']} | "
        f"Pending: {stats['pending']} | "
        f"Not Approved: {stats['not_approved']}"
    )

# Submit a new purchase requisition
def submit_requisition():

    name=staff_name_input.text().strip()
    staff_id=staff_id_input.text().strip()
    date=date_input.date().toString("dd/MM/yyyy")

    # Check staff information
    if not name or not staff_id:
        QMessageBox.warning(
            window,
            "Missing Information",
            "Please enter staff name and staff ID."
        )
        return

    # Check purchase items
    if not items:
        QMessageBox.warning(
            window,
            "Missing Items",
            "Please add at least one item."
        )
        return

    # Create the requisition object
    request=Requisition(date, staff_id, name)

    # Calculate the total and check approval
    request.add_requisition(items)
    request.approve_requisition()

    # Save the requisition
    requisitions.append(request)
    update_statistics()

    # Create a new row
    row=table.rowCount()
    table.insertRow(row)

    # Prepare the requisition information
    values=[
        request.date,
        str(request.requisition_id),
        request.staff_id,
        request.staff_name,
        f"${request.total:.2f}",
        request.status,
        request.approval_reference or "Not available"
    ]

    # Display each value in the table
    for column, value in enumerate(values):
        table.setItem(row, column, QTableWidgetItem(value))

    # Prepare the reference for display
    reference=request.approval_reference or "Not available"

    # Display submission result
    QMessageBox.information(
        window,
        "Requisition Submitted",
        f"Requisition ID: {request.requisition_id}\n"
        f"Staff Name: {request.staff_name}\n"
        f"Total: ${request.total:.2f}\n"
        f"Status: {request.status}\n"
        f"Approval Reference: {reference}"
    )

    # Clear the form for the next purchase
    items.clear()
    items_label.setText("Items: 0 | Total: $0.00")
    staff_name_input.clear()
    staff_id_input.clear()


# Connect Submit button to the function
submit_button.clicked.connect(submit_requisition)

# Create manager action buttons
manager_layout=QHBoxLayout()

approve_button=QPushButton("Approve Selected")
reject_button=QPushButton("Not Approve Selected")

# Place buttons side by side
manager_layout.addWidget(approve_button)
manager_layout.addWidget(reject_button)

# Add them to the GUI
layout.addLayout(manager_layout)

# Process a manager's decision
def manager_decision(decision):

    row=table.currentRow()

    if row==-1:
        QMessageBox.warning(
            window,
            "No Selection",
            "Please select a requisition first."
        )
        return

    # Find the corresponding requisition
    request=requisitions[row]

    if request.status !="Pending":
        QMessageBox.warning(
            window,
            "Invalid Action",
            "Only pending requisitions can be changed."
        )
        return
   
 # Apply the manager's decision
    request.respond_requisition(decision)

    # Update the status in the table
    table.item(row, 5).setText(request.status)

    # Update the approval reference
    reference = request.approval_reference or "Not available"
    table.item(row, 6).setText(reference)
    
    
# Refresh statistics after the manager's decision
    update_statistics()

    QMessageBox.information(
        window,
        "Manager Response",
        f"Requisition {request.requisition_id}\n"
        f"Status: {request.status}"
    )
approve_button.clicked.connect(
    lambda: manager_decision("Approved")
)

reject_button.clicked.connect(
    lambda: manager_decision("Not approved")
)

layout.addStretch()

# Attach the layout to the window
window.setLayout(layout)

window.show()

sys.exit(app.exec())