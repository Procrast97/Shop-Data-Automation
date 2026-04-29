from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, SelectField, DateField
from wtforms.validators import DataRequired, URL, Optional, Regexp


#CREATE USER ACCOUNT:
class RegisterForm(FlaskForm):
    ##Username
    username = StringField('Username', validators=[DataRequired()])
    ##Email
    email = EmailField('Email', validators=[DataRequired()])
    ##Password
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

#LOGIN USER:
class LoginForm(FlaskForm):
    ##Email
    email = StringField('Email', validators=[DataRequired()])
    ##Password
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

#GENERATE REPORT(add a 'sort by' section as well):
class GenReportForm(FlaskForm):
    ##Shop names (or all)
    shops = SelectField('Shops', choices=[], coerce=str)
    ##Shop location
    shop_loc = SelectField('Shop Location', choices=[], coerce=str )
    ##Period (5, 10, 15, 30 days)
    set_period = SelectField('Period', choices=[
        ("1", "1"), ("2", "5"), ("3", "10"),
        ("4", "15"), ("5", "30")
    ], validators=[Optional()])
    ## Give the user an option to insert a custom date:
    custom_date = BooleanField(label='Custom Date Range')
    from_date = StringField('From:', validators=[Optional()])
    to_date = StringField('To:', validators=[Optional()])
    ###Optional - Sort by (Item name, top 100 items (by price, etc.), time, etc.
    # sort = StringField('Sort', validators=[DataRequired()])
    submit = SubmitField('Generate Report')

    """Inserting validation to handle conditional requirements ('Optionals')."""
    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False

        # Custom_date is checked, the from and to is a requirement
        if self.custom_date.data:
            if not self.from_date.data or not self.to_date.data:
                self.from_date.errors.append("Both From and To dates are required.")
                return False

        else: #Set period selector is required
            if not self.set_period.data:
                self.set_period.errors.append("Please make a selection or use custom date.")
                return False

        return True

##ADD SHOP OR ITEMS:
class AddTypeForm(FlaskForm):
    add_shops = BooleanField('Add Shops')
    add_items = BooleanField('Add Items')

#ADD SHOPS:
class AddShopForm(FlaskForm):
    ##URL CHOICE
    url_choice = SelectField('Existing URL', choices=[], coerce=int, validators=[Optional()])
    ##URL
    shop_url = StringField('URL', validators=[
        Optional(),
        URL(message="Please ensure your URL starts with 'https://', the shop url name is correct, e.g. 'lomb', "
                    "and NB ensure it ends with, '/box_login.asp' and nothing else."),
        Regexp(r'https://', message= "URL must start with 'https://'."),
        Regexp(r'.*\/box_login.asp', message= "Your URL must only end with '/box_login.asp' - Example = 'https://www.one-pos.com/uniquecube/box_login.asp'.")])
    ##Shop name
    shop_name = StringField('Shop Name', validators=[DataRequired()])
    ##Shop Location
    shop_loc = StringField('Location', validators=[DataRequired()])
    ##Submit addition
    submit = SubmitField('Add Shop')

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False
        if (not self.url_choice.data or self.url_choice.data == 0) and not self.shop_url.data:
            self.shop_url.errors.append("Please either select and existing URL or insert a new one.")
            return False
        return True

#ADD ITEM DATA MANUALLY:
class AddItemsForm(FlaskForm):
    date =  StringField('Date of sale (Format - DD/MM/YYYY)', validators=[Optional()])
    shop_loc = SelectField('Shop Location', choices=[], coerce=int)
    customer = StringField('Customer', validators=[Optional()])
    description = StringField('Description', validators=[Optional()])
    product_id = StringField('Product ID', validators=[Optional()])
    qty = StringField('Quantity', validators=[Optional()])
    price = StringField('Price', validators=[Optional()])
    submit = SubmitField('Add Item')


##REMOVE SPECIFIC ITEM:
class RemoveItemForm(FlaskForm):
    shop_abbr = SelectField('Shop Name', choices=[], coerce=int)
    shop_location = SelectField('Shop Location', choices=[], coerce=int)
    date = DateField('Date', validators=[Optional()])
    item_field = SelectField('Item', choices=[], coerce=int)
    remove = SubmitField('Remove Item')

#REMOVE SHOP/URL:
class RemoveShopForm(FlaskForm):
    url = SelectField('URL', choices=[], coerce=int)
    url_check = BooleanField('Remove URL')
    curr_loc = SelectField('Shop Location', choices=[], coerce=int)
    shop_check = BooleanField('Remove Location')
    submit = SubmitField('Remove')

#AMEND EXISTING SHOPS/URL:
class AmendForm(FlaskForm):
    #Selecting which URl and corresponding shop to be amended:
    shop_url = SelectField("Select a URL", choices=[], coerce=int)
    curr_loc = SelectField("Shop Location", choices=[], coerce=int)

    #The new amended information to be submitted:
    new_url = StringField('New URL')
    new_loc = StringField('New Shop Location')

    submit = SubmitField('Save Changes')

# #DISCREPANCIES (meaning display all deductions made throughout the month)

