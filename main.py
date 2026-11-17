from requisition import Requisition

# Create our first requisition
request1=Requisition(
    "17/11/2026",
    "FN19",
    "John Paul"
)
# Create our second requisition
request2=Requisition(
    "17/11/2026",
    "FN20",
    "Tracy Brown"
)

# David's request is left pending

# Add items for John Paul
request1.add_requisition([
    {"name": "Keyboard", "price": "150.00"},
    {"name": "Mouse", "price": "100.00"},
    {"name": "Headphones", "price": "200.00"}
])

# Add items for Tracy Brown
request2.add_requisition([
    {"name": "Monitor", "price": "400.00"},
    {"name": "Printer", "price": "350.00"}
])


# Third requisition: exactly $500
request3 = Requisition("17/11/2026", "FN15", "Emma Wilson")

request3.add_requisition([
    {"name": "Office Chair", "price": "500.00"}
])

# Fourth requisition: just below $500
request4 = Requisition("17/11/2026", "FN02", "Catlin White")

request4.add_requisition([
    {"name": "Office Supplies", "price": "499.99"}
])

# Fifth requisition: remains pending
request5 = Requisition("17/11/2026", "FN21", "David Smith")

request5.add_requisition([
    {"name": "Laptop", "price": "950.00"}
])

# Automatically check both requisitions

request1.approve_requisition()
request2.approve_requisition()
request3.approve_requisition()
request4.approve_requisition()
request5.approve_requisition()

# Display first requisition
print("First Requisition")
print("Name:", request1.staff_name)
print("ID:", request1.requisition_id)
print("Status:", request1.status)

print()

# Display second requisition
print("Second Requisition")
print("Name:", request2.staff_name)
print("ID:", request2.requisition_id)
print("Status:", request2.status)
print()
print("John's Total: $", request1.total)
print("Tracy's Total: $", request2.total)

print()
print("----- Approval Results -----")

print("John's Status:", request1.status)
print("John's Reference:", request1.approval_reference)

print("Tracy's Status:", request2.status)

if request2.approval_reference is None:
    print("Tracy's Reference: Not available")
else:
    print("Tracy's Reference:", request2.approval_reference)

# Manager responds to Tracy's pending requisition
print()
print("----- Manager Response -----")

request2.respond_requisition("Approved")
# Manager rejects Emma's requisition
request3.respond_requisition("Not approved")

print("Staff Name:", request2.staff_name)
print("Requisition ID:", request2.requisition_id)
print("Total: $", request2.total)
print("Updated Status:", request2.status)
print("Approval Reference:", request2.approval_reference)


# Store all requisitions in a list
requisitions = [
    request1,
    request2,
    request3,
    request4,
    request5
]


# Calculate statistics
stats = Requisition.requisition_statistics(requisitions)

print()
print("----- Requisition Statistics -----")
print("Total Submitted:", stats["total"])
print("Approved:", stats["approved"])
print("Pending:", stats["pending"])
print("Not Approved:", stats["not_approved"])

# Display all five requisitions
print()
Requisition.display_requisitions(requisitions)
