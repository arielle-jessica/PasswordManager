def reset_password():
    global master_password_hash
    new_password = getpass.getpass("Enter a new master password: \n")
    hasher = argon2.PasswordHasher()
    master_password_hash = hasher.hash(new_password)
    with open('master_password_hash.txt', 'w') as f:
        f.write(master_password_hash)
    print("Password reset successful. You can now log in with your new password.\n")