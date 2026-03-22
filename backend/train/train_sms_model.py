from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import torch
import os

def generate_synthetic_sms_data():
    legit_texts = [
        "Hey, are we still on for coffee later?",
        "Don't forget to pick up groceries.",
        "Your package has been delivered to your front porch.",
        "Happy birthday! Hope you have a great day.",
        "Meeting is scheduled for 10 AM tomorrow.",
        "Can you send me that document?",
        "Dinner at 7. Sounds good?",
        "I'll call you back in 5 mins."
    ]
    phishing_texts = [
        "URGENT: Your bank account is suspended. Click http://bit.ly/update-now to verify.",
        "You won a $1000 Amazon Gift Card! Claim here: http://freecash.com",
        "Your Apple ID has been locked for security reasons. Login here to unlock: http://apple-verify.net",
        "Final Notice: Unpaid toll invoice. Pay now to avoid fees: http://toll-pay.xyz",
        "We noticed unusual activity on your card. Verify immediately: http://secure-bank-alert.com",
        "Action required: update your shipping address for pending delivery.",
        "Your Netflix subscription has expired. Renew at http://netflix-renew.tv",
        "Congratulations! You've been selected for a free cruise. Call now!"
    ]
    
    texts = legit_texts * 50 + phishing_texts * 50
    labels = [0] * len(legit_texts) * 50 + [1] * len(phishing_texts) * 50
    return {"text": texts, "label": labels}

def train_and_save_model():
    print("Loading synthetic SMS data...")
    data = generate_synthetic_sms_data()
    dataset = Dataset.from_dict(data).shuffle(seed=42)
    
    train_test = dataset.train_test_split(test_size=0.2)
    train_dataset = train_test['train']
    test_dataset = train_test['test']
    
    model_name = "distilbert-base-uncased"
    tokenizer = DistilBertTokenizer.from_pretrained(model_name)
    
    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)
    
    print("Tokenizing data...")
    tokenized_train = train_dataset.map(tokenize_function, batched=True)
    tokenized_test = test_dataset.map(tokenize_function, batched=True)
    
    print("Initializing model...")
    model = DistilBertForSequenceClassification.from_pretrained(model_name, num_labels=2)
    
    # Very basic training params just to get a saved model. 
    # Real training requires much more data/epochs.
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=2,
        per_device_train_batch_size=8,
        logging_dir='./logs',
        logging_steps=10,
        evaluation_strategy="epoch",
        save_strategy="epoch"
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_test,
    )
    
    print("Training DistilBert model...")
    trainer.train()
    
    os.makedirs('models/sms_model', exist_ok=True)
    model.save_pretrained('models/sms_model')
    tokenizer.save_pretrained('models/sms_model')
    print("Model saved to models/sms_model")

if __name__ == "__main__":
    train_and_save_model()
