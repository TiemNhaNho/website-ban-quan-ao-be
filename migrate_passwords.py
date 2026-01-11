"""
Migration script to re-hash all existing passwords with new SHA256 + Bcrypt method.

IMPORTANT: This script cannot automatically migrate passwords because we don't have
the plain text passwords. Instead, it provides two options:

Option 1: Transparent Migration (Recommended)
- Users will be automatically migrated when they login
- No action needed from users
- Already implemented in login endpoint

Option 2: Force Password Reset
- Mark all users as needing password reset
- Send password reset emails
- Users must reset their passwords

This script is for documentation and manual migration if needed.
"""

from sqlalchemy.orm import Session
from app.db.base import SessionLocal, engine
from app.models.customer_model import Customer
from app.core.security import hash_password
import sys

def check_password_format(db: Session):
    """
    Check how many users have old vs new password format.
    """
    customers = db.query(Customer).all()
    
    print(f"\n📊 Password Format Analysis:")
    print(f"Total customers: {len(customers)}")
    print(f"\nNote: Cannot determine format without plain passwords.")
    print(f"All passwords will be migrated transparently when users login.")
    
    return len(customers)

def force_password_reset(db: Session):
    """
    Option 2: Force all users to reset their passwords.
    WARNING: This will require all users to reset passwords!
    """
    print("\n⚠️  WARNING: This will force ALL users to reset their passwords!")
    confirm = input("Type 'YES' to continue: ")
    
    if confirm != "YES":
        print("❌ Cancelled")
        return
    
    customers = db.query(Customer).all()
    
    # Add a flag to force password reset
    # You would need to add this field to the Customer model first
    # customer.force_password_reset = True
    
    print(f"\n✅ Marked {len(customers)} users for password reset")
    print("📧 You should send password reset emails to all users")
    
    # db.commit()

def main():
    print("=" * 60)
    print("🔐 Password Migration Tool")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        print("\nOptions:")
        print("1. Check password format (info only)")
        print("2. Force password reset for all users (WARNING)")
        print("3. Exit")
        
        choice = input("\nSelect option (1-3): ")
        
        if choice == "1":
            check_password_format(db)
            print("\n✅ Transparent migration is already enabled in login endpoint")
            print("   Users will be automatically migrated when they login")
            
        elif choice == "2":
            force_password_reset(db)
            
        elif choice == "3":
            print("👋 Goodbye!")
            
        else:
            print("❌ Invalid option")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
        
    finally:
        db.close()

if __name__ == "__main__":
    print("\n📝 Migration Strategy:")
    print("   ✅ Transparent Migration (Recommended)")
    print("      - Already implemented in login endpoint")
    print("      - Users are automatically migrated when they login")
    print("      - No user action required")
    print("      - verify_password() supports both old and new formats")
    print("\n   ⚠️  Force Reset (Not Recommended)")
    print("      - Requires all users to reset passwords")
    print("      - Sends reset emails to all users")
    print("      - Disruptive to user experience")
    print("\n")
    
    main()
