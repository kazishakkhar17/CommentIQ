import pandas as pd
from sklearn.model_selection import train_test_split

# Fix missing notes
df = pd.read_csv('data/labeled/labeled_comments.csv')
df['notes'] = df['notes'].fillna('').astype(str).replace('nan', '')
df.to_csv('data/labeled/labeled_comments.csv', index=False)

# Re-read the clean version
df = pd.read_csv('data/labeled/labeled_comments.csv')
print('Missing values after fix:', df.isnull().sum().sum())

# Split
train_df, temp_df = train_test_split(df, test_size=0.3, random_state=42, stratify=df['emotion'])
val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42, stratify=temp_df['emotion'])

train_df.to_csv('data/labeled/train.csv', index=False)
val_df.to_csv('data/labeled/val.csv', index=False)
test_df.to_csv('data/labeled/test.csv', index=False)

print(f'Train: {len(train_df)}')
print(f'Val:   {len(val_df)}')
print(f'Test:  {len(test_df)}')