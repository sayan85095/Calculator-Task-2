import tkinter as tk
from tkinter import ttk, messagebox
import math

class Calculator:
    def __init__(self):
        self.result = 0

    def calculate(self, num1, num2, operation):
        try:
            num1 = float(num1)
            num2 = float(num2)
            
            if operation == '+':
                self.result = num1 + num2
            elif operation == '-':
                self.result = num1 - num2
            elif operation == '*':
                self.result = num1 * num2
            elif operation == '/':
                if num2 == 0:
                    raise ZeroDivisionError("Cannot divide by zero")
                self.result = num1 / num2
            elif operation == '^':
                self.result = num1 ** num2
            elif operation == 'sqrt':
                if num1 < 0:
                    raise ValueError("Cannot square root negative number")
                self.result = math.sqrt(num1)
            else:
                raise ValueError("Invalid operation")
                
            return self.result
            
        except ValueError as e:
            raise ValueError(f"Invalid input: {str(e)}")
        except ZeroDivisionError as e:
            raise ZeroDivisionError(str(e))
        except Exception as e:
            raise Exception(f"Calculation error: {str(e)}")

def run_cli_calculator():
    calc = Calculator()
    print("\nCommand Line Calculator")
    print("Available operations: +, -, *, /, ^ (power), sqrt (square root)\n")

    while True:
        try:
            # Get first number (or sqrt operand)
            num1 = input("Enter first number (leave empty for square root): ").strip()
            
            # Square root operation
            if not num1:
                num1 = input("Enter number for square root: ").strip()
                operation = 'sqrt'
                num2 = 0  # dummy value
            else:
                # Get second number for other operations
                num2 = input("Enter second number: ").strip()
                operation = input("Enter operation (+, -, *, /, ^): ").strip()
            
            result = calc.calculate(num1, num2, operation)
            print(f"\nResult: {result:.4f}\n")
            
            if input("Calculate again? (y/n): ").lower() != 'y':
                break
                
        except Exception as e:
            print(f"\nError: {e}\n")
            if input("Try again? (y/n): ").lower() != 'y':
                break

class CalculatorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Calculator")
        self.geometry("350x400")
        self.calculator = Calculator()
        
        self.create_widgets()
    
    def create_widgets(self):
        # Display
        self.display_var = tk.StringVar()
        display = ttk.Entry(
            self,
            textvariable=self.display_var,
            font=('Arial', 18),
            justify='right',
            state='readonly'
        )
        display.pack(fill=tk.X, padx=10, pady=10, ipady=10)
        
        # Button frame
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        # Button layout
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', 'C', '+',
            '√', '^', 
        ]
        
        # Create and place buttons
        for i, text in enumerate(buttons):
            row = i // 4
            col = i % 4
            
            # Adjust for extra buttons in last row
            if text in ['√', '^']:
                row = 4
                col = i - 16 + 2  # Position after 'C' and '+'

            btn = ttk.Button(
                button_frame,
                text=text,
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            # Configure row/column weights
            button_frame.rowconfigure(row, weight=1)
            button_frame.columnconfigure(col, weight=1)
        
        # Equal button
        equals = ttk.Button(
            button_frame,
            text='=',
            command=self.calculate
        )
        equals.grid(row=4, column=3, columnspan=1, padx=5, pady=5, sticky="nsew")
        
        # Configure button styles
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 14), padding=5)
        
        # Initialize calculator state
        self.reset_calculator()
    
    def reset_calculator(self):
        self.first_number = None
        self.operation = None
        self.start_new_number = True
        self.display_var.set('0')
    
    def on_button_click(self, button_text):
        current = self.display_var.get()
        
        if button_text == 'C':
            self.reset_calculator()
        elif button_text in ['√', '^']:
            self.handle_operation(button_text)
        elif button_text in ['+', '-', '*', '/']:
            self.handle_operation(button_text)
        else:
            if self.start_new_number:
                self.display_var.set(button_text)
                self.start_new_number = False
            elif current == '0':
                self.display_var.set(button_text)
            else:
                self.display_var.set(current + button_text)
    
    def handle_operation(self, operation):
        if self.display_var.get() == '0' and operation != '√':
            return
            
        if self.first_number is None:
            self.first_number = float(self.display_var.get())
            self.operation = operation
            self.start_new_number = True
        else:
            self.calculate()
            self.operation = operation
    
    def calculate(self):
        if self.first_number is None or self.operation is None:
            return
            
        try:
            second_number = float(self.display_var.get()) if not self.start_new_number else self.first_number
            
            if self.operation == '√':
                result = self.calculator.calculate(second_number, 0, 'sqrt')
            else:
                result = self.calculator.calculate(self.first_number, second_number, self.operation)
            
            self.display_var.set(f"{result:.6f}".rstrip('0').rstrip('.') if '.' in f"{result:.6f}" else str(result))
            self.first_number = result
            self.start_new_number = True
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.reset_calculator()

if __name__ == "__main__":
    print("Calculator Application")
    print("1. Command Line Interface")
    print("2. Graphical User Interface")
    
    while True:
        choice = input("Select interface (1/2): ").strip()
        if choice == '1':
            run_cli_calculator()
            break
        elif choice == '2':
            app = CalculatorGUI()
            app.mainloop()
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
