# PastryPro

## Introduction
PastryPro is an advanced inventory management system specifically designed for bakers and pastry chefs. It is a comprehensive software solution that streamlines the process of managing and tracking ingredients, supplies, and equipment in a baking or pastry kitchen.
With PastryPro, bakers can efficiently monitor and control their inventory, ensuring they have the right ingredients on hand to create delicious pastries and baked goods. The system provides real-time visibility into stock levels, expiration dates, and usage patterns, enabling bakers to make informed purchasing decisions and minimize waste.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Configuration](#configuration)
- [Development](#development)
- [Roadmap](#roadmap)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Contact Information](#contact-information)
- [Additional Documentation](#additional-documentation)

## Installation
To install PastryPro on your local development environment, follow these steps:

1. Clone the repository from GitHub:   
```bash
git clone https://github.com/sundayirvine-code/pastrypro.git
```
2. Install the required dependencies:  
```bash
pip install -r requirements.txt
```
3. Configure the environment variables:  
Edit the `.env` file and provide the necessary configuration if you are using a Mysql databse. Otherwise comment out the Mysql databse configuration on the `app.py` file like so and use sqlite as the databse.:  
```python
#app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
```  
4. Start the PastryPro server: 
```python
python app.py
```  

## Usage
PastryPro provides a user-friendly interface to manage and explore pastry inventory. Here are some examples of how to use PastryPro:

1. **Sign up:**
   - Navigate to the PastryPro landing page.
   - Click on the "Sign Up" link.
   - Fill out the required information to create a new account.

2. **Log in:**
   - After signing up, you will be directed to the login page.
   - Enter your credentials (username and password) to access your account.

3. **Manage Pastry Stock:**
   - On the inventory page, create custom categories to organize your stock products by clicking the "Category +" button.
   - Create stock items by clicking the "Add Stock Item +" button.
   - Provide information about each stock item, such as name, quantity, price, and description.

4. **Create Baked Products:**
   - Navigate to the bake route by clicking the "Price Calc" button on the inventory page.
   - Click the "Create Baked Product" button on the bake page.
   - In the pop-up window, define the various baked products you intend to bake (e.g., biscuits, cakes, bread).

5. **Bake a Specific Product:**
   - Select a baked product from the available options on the bake page.
   - Choose the desired units of measurement.
   - Specify the quantity to be baked and enter the costs incurred during the baking process.
   - Search for and select individual stock items (ingredients) required for the chosen product.
   - Enter the quantity of each ingredient used in the baking process.
   - The price calculator automatically calculates and appends the cost price based on the selected ingredients.

6. **Calculate Selling Price:**
   - Add all the necessary ingredients for your product.
   - The system automatically calculates the total cost price.
   - Click the "Calculate Selling Price" button.
   - A selling price with a 40 percent profit margin is generated.

7. **Update Database:**
   - After baking the product, all the relevant information is updated in the database.

8. **View Analytics:**
   - Head over to the analytics page to view various analytics related to your baking process.
   - Gain insights into the performance, profitability, and trends of your pastry production.



## Technologies Used

This project was developed using the following technologies:

- **HTML:** The standard markup language for creating the structure and content of web pages. [Learn more](https://developer.mozilla.org/en-US/docs/Web/HTML)

- **CSS:** A stylesheet language used for describing the presentation of a document written in HTML. [Learn more](https://developer.mozilla.org/en-US/docs/Web/CSS)

- **Bootstrap:** A popular CSS framework that provides pre-designed responsive components and styles to simplify web development. [Learn more](https://getbootstrap.com/)

- **Python:** A versatile and powerful programming language used for server-side development, data processing, and automation. [Learn more](https://www.python.org/)

- **JavaScript:** A programming language that enables dynamic and interactive behavior on web pages. [Learn more](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

- **jQuery:** A fast and concise JavaScript library that simplifies HTML document traversal, event handling, and animation. [Learn more](https://jquery.com/)

- **Flexbox:** A CSS layout module that provides a flexible way to distribute and align elements within a container. [Learn more](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout)

- **CSS Grid:** A powerful two-dimensional layout system in CSS that allows for the creation of complex grid-based layouts. [Learn more](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout)


## Configuration

To configure the project and connect it to your database, follow these steps:

1. Open the `.env` file in the project directory.

2. Locate the `DATABASE_URI` variable and replace its value with your unique database information.

   Example:
   DATABASE_URI=mysql+pymysql://username:password@localhost:3306/mydatabase  

Make sure to update the username, password, host, and database name based on your own configuration.

3. Save the changes to the `.env` file.

By updating the `DATABASE_URI` with your own database information, the project will be able to establish a connection and interact with your database accordingly.

Note: Ensure that you have the necessary database permissions and that the database is accessible from the environment where the project is running.  

## Roadmap
We have an exciting roadmap for PastryPro, with several upcoming features and enhancements planned. Here are some of the key milestones and future plans:

1. Enhanced User Interface: We are continuously working on improving the user interface to make it more intuitive and user-friendly. This includes refining the design, optimizing layouts, and adding new visual elements.

2. Mobile App Integration: We are planning to develop a mobile application for PastryPro, allowing users to manage their pastry inventory and baking processes on-the-go. The mobile app will provide a seamless experience with all the features available in the web version.

3. Order Management: We are working on adding an order management system to PastryPro. This feature will enable users to receive and manage customer orders, track order status, and generate invoices.

4. Recipe Management: We plan to introduce a recipe management module, where users can create and store their pastry recipes. This feature will include the ability to define ingredients, quantities, instructions, and nutritional information for each recipe.

5. Integration with E-commerce Platforms: We aim to integrate PastryPro with popular e-commerce platforms, such as Shopify or WooCommerce. This integration will allow users to synchronize their pastry products, inventory, and pricing with their online stores.

6. Advanced Analytics: We will be expanding the analytics capabilities of PastryPro to provide more in-depth insights into sales trends, profitability, and ingredient usage. Users will be able to generate detailed reports and visualize data using charts and graphs.

Stay tuned for these exciting updates as we continue to develop and enhance PastryPro to meet the needs of pastry professionals and enthusiasts alike!

## Troubleshooting
Here are some common issues or errors that users may encounter while using PastryPro, along with their respective solutions or workarounds:

1. Database Connection Errors: If users encounter issues connecting to the database, they should verify that the database URI in the .env file is correctly configured with their unique database information. Make sure the username, password, host, and database name are accurate. If the issue persists, users can check their network connection and ensure that the database server is accessible.

2. Missing Dependencies: If users encounter missing dependencies or module import errors, it's recommended to verify that all the required dependencies are installed. They can run the command pip install -r requirements.txt to install the necessary packages specified in the project's requirements.txt file.

3. CSS or Styling Issues: If the user interface appears distorted or the styling is not being applied correctly, it could be due to caching or loading issues. In such cases, users can try clearing their browser cache or force-refresh the page (Ctrl + Shift + R or Cmd + Shift + R) to ensure the latest styles are loaded.

4. Authentication Problems: If users are unable to log in or access certain features, they should double-check their login credentials and ensure they are using the correct username and password. If forgotten, there is typically a "Forgot Password" option available to reset the password.

5. Performance or Speed Issues: If PastryPro is running slowly or experiencing performance issues, it could be due to various factors such as server load, network congestion, or inefficient code. Users can try refreshing the page, closing unnecessary browser tabs, or reaching out to the support team if the problem persists.

## License
PastryPro is distributed under the MIT License.

The MIT License is a permissive open-source license that allows you to use, modify, and distribute the software, both commercially and non-commercially, as long as you include the original license in your distribution. It provides flexibility and freedom for developers to use PastryPro in their projects.
For more information about the MIT License, please visit opensource.org/licenses/MIT.

## Acknowledgements
We would like to express our gratitude to the following individuals, projects, and resources that have contributed to the development of PastryPro:

OpenAI: We would like to thank OpenAI for providing the underlying technology that powers ChatGPT, which has been instrumental in assisting us throughout the development process.

Bootstrap: We are grateful to the Bootstrap framework for its robust and responsive CSS and JavaScript components, which have greatly contributed to the overall design and user experience of PastryPro.

jQuery: Our appreciation goes to the jQuery library for simplifying the process of manipulating HTML documents, handling events, and creating dynamic web content within PastryPro.

Flexbox: We would like to acknowledge the Flexbox layout module for its powerful features that have enabled us to create flexible and responsive layouts in PastryPro.

CSS Grid: Our thanks go to the CSS Grid layout module for providing a powerful grid system that has facilitated the creation of complex and grid-based layouts in PastryPro.

We also extend our gratitude to all the individuals, developers, and communities who have contributed to the open-source projects, libraries, and resources that we have utilized in the development of PastryPro. Your work and dedication have played a significant role in the success of this project.

## Contact Information
For any inquiries or feedback regarding PastryPro, you can reach out to the project maintainer, Irvine Sunday, using the following contact information:

GitHub: sundayirvine-code
LinkedIn: Irvine Sunday
Portfolio: Irvine Sunday's Portfolio
Feel free to connect with us through these platforms for any questions, suggestions, or collaboration opportunities. We look forward to hearing from you!
