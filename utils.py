def prompt_user():
    while True:
        product = input("Enter the tech product you want to analyze: ").strip()
        if product:
            return product
        print("Please enter a valid product name.")
