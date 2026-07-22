import pandas as pd
import os

def main():
    # Load data
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    dashboard_dir = os.path.join(base_dir, 'dashboard')
    
    print("Loading datasets...")
    orders = pd.read_csv(os.path.join(data_dir, 'orders_dataset.csv'))
    order_items = pd.read_csv(os.path.join(data_dir, 'order_items_dataset.csv'))
    order_reviews = pd.read_csv(os.path.join(data_dir, 'order_reviews_dataset.csv'))
    products = pd.read_csv(os.path.join(data_dir, 'products_dataset.csv'))
    
    # 1. Cleaning products dataset
    print("Cleaning products dataset...")
    products.rename(columns={
        'product_name_lenght': 'product_name_length',
        'product_description_lenght': 'product_description_length'
    }, inplace=True)
    products.dropna(subset=['product_category_name', 'product_name_length', 'product_description_length', 'product_photos_qty'], inplace=True)
    
    # 2. Cleaning orders dataset
    print("Cleaning orders dataset...")
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
    orders.dropna(subset=['order_delivered_customer_date'], inplace=True)
    
    # Calculate delivery time in days
    orders['deliveryTime'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']).dt.total_seconds() / (24 * 3600)
    
    # Filter delivery time 0-50 days as per notebook insight
    orders = orders[(orders['deliveryTime'] >= 0) & (orders['deliveryTime'] <= 50)]
    
    # 3. Clean reviews
    print("Cleaning reviews dataset...")
    order_reviews.dropna(subset=['review_score'], inplace=True)
    
    # Merge datasets
    print("Merging datasets...")
    merged = pd.merge(order_reviews[['order_id', 'review_score']], 
                      orders[['order_id', 'deliveryTime']], 
                      on='order_id', how='inner')
                      
    merged = pd.merge(merged, order_items[['order_id', 'product_id']], on='order_id', how='inner')
    merged = pd.merge(merged, products[['product_id', 'product_description_length', 'product_photos_qty']], on='product_id', how='inner')
    
    merged = merged.drop_duplicates(subset=['order_id', 'product_id', 'review_score'])
    
    # Select final columns to save space
    final_df = merged[['review_score', 'product_description_length', 'product_photos_qty', 'deliveryTime']]
    
    out_path = os.path.join(dashboard_dir, 'main_data.csv')
    final_df.to_csv(out_path, index=False)
    print(f"Data preprocessed successfully and saved to {out_path}")
    print(f"Final dataset shape: {final_df.shape}")

if __name__ == "__main__":
    main()
