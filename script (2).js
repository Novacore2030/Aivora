const pageContent = document.getElementById("pageContent");
const pageTitle = document.getElementById("pageTitle");

const pages = {
  Dashboard: `
    <div class="cards">
      <div class="card">
        <p>Total Customers</p>
        <h2>120</h2>
      </div>

      <div class="card">
        <p>Active Subscriptions</p>
        <h2>85</h2>
      </div>

      <div class="card">
        <p>Total Revenue</p>
        <h2>₹45,000</h2>
      </div>

      <div class="card">
        <p>Pending Invoices</p>
        <h2>12</h2>
      </div>
    </div>

    <div class="welcome">
      <h2>Subscription Management</h2>
      <p>Manage your customers, products and subscriptions in one place.</p>
      <button onclick="showPage('Customers')">View Customers</button>
    </div>
  `,

  Customers: `
    <div class="welcome">
      <h2>Customer Management</h2>
      <p>Add and manage your customers.</p>

      <input id="customerName" placeholder="Customer name">
      <input id="customerEmail" placeholder="Email address">
      <input id="customerID" placeholder="Customer ID">
      <input id="phoneno" placeholder="phoneno">
      <input id="address" placeholder="address">
      <input id="password" placeholder="password">
      <button onclick="addCustomer()">Add Customer</button>
    </div>

    <div class="card table-card">
      <h2>Customer List</h2>
      <div id="customerList"></div>
    </div>
  `,

  Products: `
    <div class="welcome">
      <h2>Product Management</h2>
      <p>Add and manage products offered by Brightloop.</p>

      <input id="productName" placeholder="Product name">
      <input id="productID" placeholder="Product ID">
      <input id="productPrice" type="number" placeholder="Price (₹)">
      <input id="productCategory" placeholder="Product category">

      <textarea id="productDescription" placeholder="Product description"></textarea>

      <button onclick="addProduct()">+ Add Product</button>
    </div>

    <div class="card">
      <h2>Product List</h2>
      <div id="productList"></div>
    </div>
`,
    

    Plans: `
    <div class="welcome">
      <h2>Choose Your Plan</h2>
      <p>Explore our plans and select the one that suits you.</p>
    </div>

    <div id="availablePlans" class="cards"></div>
  `,

  Subscriptions: `
    <div class="welcome">
      <h2>My Subscriptions</h2>
      <p>Manage your purchased subscription plans.</p>
    </div>

    <div id="mySubscriptions" class="cards"></div>
  `,

  Invoices: `
    <div class="welcome">
      <h2>Invoices</h2>
      <p>View and manage customer invoices.</p>
      <button onclick="alert('Invoice creation coming soon!')">+ Create Invoice</button>
    </div>
  `,

  Payments: `
    <div class="welcome">
      <h2>Payments</h2>
      <p>Monitor payment records and transactions.</p>
    </div>
  `,

  Reports: `
    <div class="welcome">
      <h2>Reports & Analytics</h2>
      <p>View your business performance and subscription statistics.</p>
    </div>
  `
};

let customers = [];

function showPage(page) {
  pageTitle.textContent = page;
  pageContent.innerHTML = pages[page];

  document.querySelectorAll("nav button").forEach(button => {
    button.classList.toggle(
      "active",
      button.dataset.page === page
    );
  });

  if (page === "Customers") {
  displayCustomers();
}

if (page === "Plans") {
  displayAvailablePlans();
}
if (page === "Subscriptions") {
  displayMySubscriptions();
}
}

function addCustomer() {
  const name = document.getElementById("customerName").value.trim();
  const email = document.getElementById("customerEmail").value.trim();
  const id = document.getElementById("customerID").value.trim();
  const phoneno = 
document.getElementById("phoneno").value.trim();
  const address = document.getElementById("address").value.trim();
  const password = document.getElementById("password").value.trim();
  if (!name || !email) {
    alert("Please enter both name and email!");
    return;
  }

  customers.push({ name, email, id , phoneno, address, password });

  displayCustomers();

  document.getElementById("customerName").value = "";
  document.getElementById("customerEmail").value = "";
  document.getElementById("customerID").value = "";
  document.getElementById("phoneno").value = "";
  document.getElementById("address").value = "";
  document.getElementById("password").value = "";
  alert("Customer added successfully!");
}

function displayCustomers() {
  const list = document.getElementById("customerList");

  if (customers.length === 0) {
    list.innerHTML = "<p>No customers added yet.</p>";
    return;
  }

  list.innerHTML = customers.map((customer, index) => `
    <p class="customer-row">
      ${index + 1}. <strong>${customer.name}</strong>
      — ${customer.email}
    </p>
  `).join("");
}

document.querySelectorAll("nav button").forEach(button => {
  button.addEventListener("click", () => {
    showPage(button.dataset.page);
  });
});

showPage("Dashboard");
let customerList = [];

function addNewCustomer() {
  const name = document.getElementById("newCustomer").value.trim();
  const email = document.getElementById("newEmail").value.trim();
  const id = 
document.getElementById("newID").value.trim();
  const phoneno = 
document.getElementById("newphoneno").value.trim();
  const address = document.getElementById("newaddress").value.trim();
  const password = document.getElementById("newpassword").value.trim();
  if (!name || !email) {
    alert("Please enter name and email!");
    return;
  }

  customerList.push({ name, email,id,phoneno,address,password});

  document.getElementById("customerDisplay").innerHTML =
    customerList.map(customer => `
      <div class="card">
        <h3>${customer.name}</h3>
        <p>${customer.email}</p>
        <p>${customer.id}</p>
        <p>${customer.phoneno}</p>
        <p>${customer.address}</p>
        <p>${customer.password}</p>
      </div>
    `).join("");

  document.getElementById("newCustomer").value = "";
  document.getElementById("newEmail").value = "";
  document.getElementById("newID").value = "";
  document.getElementById("newphoneno").value = "";
  document.getElementById("newaddress").value = "";
  document.getElementById("newpassword").value = "";
  
  
}
let availablePlans = [
  {
    name: "Basic",
    price: 199,
    duration: "Monthly",
    features: "Essential features"
  },
  {
    name: "Standard",
    price: 499,
    duration: "Monthly",
    features: "Advanced features"
  },
  {
    name: "Premium",
    price: 999,
    duration: "Monthly",
    features: "All premium features"
  }
];

function addPlan() {
  const name = document.getElementById("planName").value.trim();
  const price = document.getElementById("planPrice").value;
  const duration = document.getElementById("planDuration").value;

  if (!name || !price || Number(price) <= 0) {
    alert("Please enter a valid plan name and price!");
    return;
  }

  plans.push({ name, price, duration });

  document.getElementById("planList").innerHTML =
    plans.map(plan => `
      <div class="card">
        <h3>${plan.name}</h3>
        <p>₹${plan.price} / ${plan.duration}</p>
      </div>
    `).join("");

  document.getElementById("planName").value = "";
  document.getElementById("planPrice").value = "";

  alert("Plan created successfully!");
}
function displayAvailablePlans() {
  const container = document.getElementById("availablePlans");

  container.innerHTML = availablePlans.map((plan, index) => `
    <div class="card">
      <h2>${plan.name}</h2>
      <h3>₹${plan.price} / ${plan.duration}</h3>
      <p>${plan.features}</p>
      <button onclick="choosePlan(${index})">
        Choose Plan
      </button>
    </div>
  `).join("");
}
let mySubscriptions = [];

function choosePlan(index) {
  const selectedPlan = availablePlans[index];

  const confirmPlan = confirm(
    `You selected ${selectedPlan.name} for ₹${selectedPlan.price}. Proceed to demo payment?`
  );

  if (!confirmPlan) return;

  const payment = confirm("Demo payment successful?");

  if (!payment) {
    alert("Payment not completed. Your subscription was not activated.");
    return;
  }

  mySubscriptions.push({
    name: selectedPlan.name,
    price: selectedPlan.price,
    duration: selectedPlan.duration,
    status: "Active",
    startDate: new Date().toLocaleDateString()
  });

  alert("Payment successful! Your subscription is now active.");
}
function displayMySubscriptions() {
  const container = document.getElementById("mySubscriptions");

  if (mySubscriptions.length === 0) {
    container.innerHTML = `
      <div class="card">
        <h3>No active subscriptions yet</h3>
        <p>Choose a plan from the Plans section to get started.</p>
        <button onclick="showPage('Plans')">Explore Plans</button>
      </div>
    `;
    return;
  }

  container.innerHTML = mySubscriptions.map(sub => `
    <div class="card">
      <h2>${sub.name}</h2>
      <h3>₹${sub.price} / ${sub.duration}</h3>
      <p>Start Date: ${sub.startDate}</p>
      <p>Status: ${sub.status}</p>
    </div>
  `).join("");
}
