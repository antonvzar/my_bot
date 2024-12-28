# **Category and Product Selector Bot**

This Telegram bot provides an intuitive interface for browsing a categorized inventory of products, including brands and series, with dynamic interaction. It utilizes Firebase as the database backend to store and retrieve product information.

## **Installation Instructions**

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### Step 2: Install Dependencies
```bash
pip install aiogram firebase-admin
```

### Step 3: Run the bot
```bash
python bot.py
```

## **Features**

### 1. **Category Selection**
- Upon starting the bot or selecting "Categories" from the main menu, users can view a list of available product categories (e.g., Shoes, Jackets, Accessories).
- The categories are dynamically retrieved from the Firebase database.

### 2. **Brand Filtering**
- After selecting a category, users are presented with a list of available brands within that category.
- The bot dynamically generates brand options based on the data in Firebase.

### 3. **Series Browsing**
- Selecting a brand will display a list of series for that brand.
- The bot filters and organizes the series data dynamically, showing all available options for the chosen brand.

### 4. **Series Details**
- After selecting a specific series, users can view detailed information, including:
  - **Brand name**
  - **Series name**
  - **Price**
- The bot provides a clear and concise breakdown of each product.

### 5. **Dynamic Database Updates**
- The bot integrates with Firebase to fetch real-time data. If new categories, brands, or series are added to the database, they are immediately reflected in the bot's options.

### 6. **Admin Functionality**
- Admins can add new products directly through the bot using commands like `/additem category brand series price`.

### 7. **Navigation**
- Users can navigate back to the previous menu at any time using "⬅ Back" buttons.
- The bot ensures a seamless and user-friendly experience.

---

## **Database Structure**

The bot uses Firebase Realtime Database with the following structure:

```json
{
  "categories": {
    "shoes": {
      "item1": {
        "brand": "Nike",
        "series": "Air Max",
        "price": 120
      },
      "item2": {
        "brand": "Adidas",
        "series": "Ultraboost",
        "price": 150
      }
    },
    "jackets": {
      "item1": {
        "brand": "North Face",
        "series": "Thermoball",
        "price": 200
      }
    }
  }
}
