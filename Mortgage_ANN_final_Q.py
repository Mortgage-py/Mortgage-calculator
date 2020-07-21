#  Title         : Annuity Mortgage 
#  Project       : Interest over mortgage lifetime
#  Task          : Estimate monthly expenses and changing housing prices over lifetime

#  Author        : Jasper Stokkermans           - https://www.linkedin.com/in/jhastokkermans/
#  Department    : Private
#  Date          : July 2020


# [ Distribution and/or commercial usage of this file without written permission is not allowed ]
# [ A free copy can be obtained by contacting the author ]

# [Disclaimer: I'm by no means a financial advisor, nor a real estate professional. Usage of script at own resposibility.]
#%%
# =============================================================================
# Import libraries
# =============================================================================

from IPython import get_ipython
def ___reset___(): get_ipython().magic('reset -sf')

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pr          = print         ; print('\n'*50)        ; t = time.time()   # Start timer
#%% [A]         - TAKING OUT A MORTGAGE LOAN
#-----------------------------------------------------------------------------
#   Set the value of the home you are looking to buy

#   Real estate properties
home_value                  = float(input("\n Enter the property value [€]: "))     # [€] Value of real estate
notional_rental_value       = 1.10 * home_value                                     # [€] Home value taxatation by government for notional tax, assume 10% above to be cponservative

home_area                   = float(input("\n Enter the property area [m]: "))      # [m] Area property
garden_area                 = float(input("\n Enter the garden area [m]: "))        # [m] Area garden

mortgage_rate_ann           = float(input("\n Enter annual mortgage interest rate [%]: "))/100      # [%] Interest rate on annuity mortgage loan 
years_ann                   = float(input("\n Enter the mortgage lifetime [y]: "))
down_payment_percent        = float(input("\n Enter the downpayment [%]: "))/100                    # [%] Percentage downpayment on real estate, own money                   
family_loan                 = float(input("\n Family bank construction [€]: "))                     # [€] Loan from family

levies                      = float(input("\n Levies (VVE) [€]: "))                                 # [€/month] Monthly maintenance reservation budget (VVE), opstalverzekering +-€55/m
levies                      = int(levies)

# Future valuation
yearly_growth_rate          = float(input("\n Yearly property value growth rate. (negative for decrease) [%]: "))  # [%/y] Average yearly increase in price of property
pr('\n'*5) 

real_estate_tax_percentage  = 0.0551/100                                            # [%] 

#%% [B]         - FAMILY BANK      

# NB: Only valid in Dutch law!   
# If not taxable in the Netherlands, set family_loan = 0

#-----------------------------------------------------------------------------

first_tax_bracket           = 0.3735                        # [%] First tax bracket income tax, second bracket is 0.4950

if family_loan == 0:
    pr('No family bank construction'+ 2*'\n')
    
if family_loan > 0:
    pr("*) Family bank construction" +  '\n')

    opt_family_interest_rate    = 5515/(family_loan)            # [%] Optimized family bank interest rate. Max tax return
    max_family_interest_rate    = 0.05

    if opt_family_interest_rate > max_family_interest_rate:     # [%] Max interst rate family bank is not allowed to exceed government set value
        opt_family_interest_rate = max_family_interest_rate


# Year 1
    family_interest             = family_loan * opt_family_interest_rate        # [€] Interest  paid to family 
    
    tax_return_family_interest  = first_tax_bracket * family_interest           # [€] 

    donation_family             = min(family_interest, 5515)                    # [€] Annual tax free donation limit. Check, this should match already

    net_pay                     = family_interest - tax_return_family_interest - donation_family

    family_interest_after_tax   = net_pay / family_loan



    pr("a) Family loan                                 = " + "€ " + str( round(family_loan)) )
    pr("b) Annual interest family loan                 = " + "€   " + str( round(family_interest )) + "   (at " +  str( round(opt_family_interest_rate*100,2)) + "%)" )
    pr("c) Tax return family interest                  = " + "€   " + str( round(tax_return_family_interest)) )
    pr("d) Net payment family bank year                = " + "€  " + str( round(net_pay)) + '\n')
    pr("e) Family loan interest rate after tax return  =    " +  str( round(family_interest_after_tax*100,2)) + " %" + 3*'\n')


#%% [C]         - CALCULATE THE VAUE OF THE DOWNPAYMENT
    
down_payment = home_value * down_payment_percent + family_loan           # [€] Downpayment on real estate, own money   

#   Calculate the value of the mortgage loan required after the down payment
mortgage_loan_ann = home_value - down_payment                            # [€] 

pr("Property:" + '\n')
pr("1) Value real estate                = " + "€     "   +str(round(home_value)))
pr("    Home area                       = " + "m2    "   +str(round(home_area)))
pr("    Price per square meter inside   = " + "€/m2  "   +str(round(home_value/home_area)))
pr("    Price per square meter total    = " + "€/m2  "   +str(round(home_value/(garden_area+home_area))) + '\n')
pr("2) Initial Down Payment             = " +"€     "   + str(round(down_payment)) + '\n')
pr("3) Mortgage Loan                    = " +"€     "   + str(round(mortgage_loan_ann)) +  "  (at " + str(mortgage_rate_ann*100)  + "%)" + 3*'\n')


#%% [D]         - COSTS

# Fixed costs
tax                         = 0.02 * home_value     # [€] Real estate transfer tax [2%]
notary_costs                = 1500                  # [€] Notary costs
mortgage_agent              = 3000                  # [€] Mortgage agent (buying side)
mortgage_consult            = 2500                  # [€] Mortgage consultant
taxation                    =  500                  # [€] Taxation cost of real estate
structural_inspection       =  500                  # [€] Evaluation real estate property
bank_guarantee              =  500                  # [€] Guarantee deposit 
mortgage_transfer           = 0000                  # [€] Transfer costs mortgage from home_1 to home_2


# Operational costs
maintenance                 = 200                   # [€/m] Maintenance property per month   
municipality_waste          = 273/12                # [€/m] Municipality levy waste water (Afvalstoffenheffing)
municipality_sewage         = 149/12                # [€/m] Municipality levy sewage system (Rioolheffing)
municipality_real_estate    = real_estate_tax_percentage * notional_rental_value /12 # [€/m] Municipality real estate tax (Gemeente belasting, onroerende zaken belasting)                
insurance                   = 25                    # [€/m] Home insurance
water                       = 25                    # [€/m] Utilities - Water
electricity                 = 125                   # [€/m] Utilities - Electricity & Gas
car_insurance               = 50                    # [€/m] Car insurance
road_tax                    = 35                    # [€/m] Road tax
health_insurance            = 110                   # [€/m] Health insurance
car_parking                 = 100/12                # [€/m] Parking allowance
tv_internet                 = 100                   # [€/m] TV, internet and phone          
groceries                   = 600                   # [€/m] Monthly groceries budget 2p


# Inventory
couch                       = 2000                  # [€] 
bed                         = 3000                  # [€]                    
tv                          = 1500                  # [€] 
dining_set                  = 1500                  # [€] 
coffeemachine               = 1500                  # [€] 
fridge                      = 1000                  # [€]


# Renovations   
double_glass                = 5000                      # [€] Upgrade windows to double glass, max. 106% of home value in mortgage if spend on renewing home. (mortage interest deductable, worth to include in mortgage)
floor                       = 1.10*0.4*home_area*65     # [€] 10% loss due to cutting, 40% of home area covered, prices from €65/m
various                     = 2500                      # [€] Paint, LED lamps, (kitchen-) equipment, small furnature etc etc
kitchen                     = 0000                      # [€] New kitchen. Approximately €10.000, again can (partly) be included into mortgage. (Bouwdepot)   


# Combined costs
fixed_costs                 = tax + notary_costs + mortgage_agent + mortgage_consult + taxation + structural_inspection + bank_guarantee + mortgage_transfer
renovations                 = double_glass + floor + kitchen + various
inventory                   = couch + bed + tv + dining_set + coffeemachine + fridge
operational                 = maintenance + municipality_waste + municipality_sewage + municipality_real_estate + insurance + water + electricity + car_parking + groceries + tv_internet + car_insurance + road_tax + 2*health_insurance 
tax_refund_y1               = ( mortgage_consult + notary_costs/2 + taxation ) * (1 - first_tax_bracket)  # [€] Expected tax refund in year 1


pr("Initial Costs:" + '\n')

pr("4) Real estate costs                 =    "  + "€ " +   str( round(fixed_costs)) + '\n')    
pr("5) Renovations                       =    "  + "€ " +   str( round(renovations)) +'\n')
pr("6) Inventory                         =    "  + "€ " +   str( round(inventory)) +'\n')
pr("7) Total initial costs               =    "  + "€ " +   str( round(fixed_costs + renovations + inventory)) + 3*'\n')

pr("*)  Estimated tax refund of initial costs y1       =  "  + "€ " + str( round (tax_refund_y1 )) )

pr("      (Inventory cost after tax refund             =  "  + "€ " + str( round (inventory - tax_refund_y1  ))  + ' ( ' + str( round (tax_refund_y1 / inventory*100 )) + '% covered by tax return))' '\n') 
pr("**) Estimated total initial costs after tax for y1 =  "  + "€ " + str( round(fixed_costs + renovations + inventory - tax_refund_y1  )) + 2*'\n')
    
 
#%%  [E]        - ANNUITY MORTGAGE - CALCULATE MONTHLY MORTGAGE PAYMENTS

# Derive the equivalent monthly mortgage rate from the annual rate
mortgage_rate_periodic_ann      = (1 + mortgage_rate_ann)**(1/12) - 1                   # [%/month] Convert annual mortgage rate to monthly rate

# Determine number of monthly payments in 30 years, label and arrange them.
mortgage_payment_periods_ann    = years_ann * 12                                        # [-] Number of periodic payments
months_ann                      = np.arange(mortgage_payment_periods_ann)                    


#%% [F]        - CALCULATE INTEREST AND PRINCIPAL PAYMENT

principal_remaining_ann = (1 - (((1 + mortgage_rate_periodic_ann) ** months_ann ) - 1 ) / (((1 + mortgage_rate_periodic_ann) ** mortgage_payment_periods_ann) - 1 )) * home_value

# Calculate the total monthly payment. This includes both prinicpal and interest.
total_periodic_payment_ann      = np.around( (mortgage_loan_ann * ( mortgage_rate_periodic_ann / (1 - ( 1 + mortgage_rate_periodic_ann)**(- (len(months_ann)))))))
initial_principal_ann           = total_periodic_payment_ann - (mortgage_loan_ann * mortgage_rate_periodic_ann) 

remaining_principal_ann         = np.round((1 - (((1 + mortgage_rate_periodic_ann) ** months_ann ) - 1 ) / (((1 + mortgage_rate_periodic_ann) ** mortgage_payment_periods_ann) - 1 )) * home_value )
interest_periodic_payment_ann   = np.round( mortgage_rate_periodic_ann * remaining_principal_ann )
principal_periodic_payment_ann  =  total_periodic_payment_ann - interest_periodic_payment_ann


# Calculate the amount of the payment that will go towards principal
principal_paid_ann              = np.cumsum(principal_periodic_payment_ann)
principal_accumulated_ann       = np.cumsum(principal_periodic_payment_ann) 
interest_accumulated_ann        = np.cumsum(interest_periodic_payment_ann) 



#%% [G]         - TAX RETURN

real_estate_tax   = real_estate_tax_percentage * notional_rental_value /12  # [€/m] Real estate tax. (Eigen woning forfait, onroerendezaken belasting)

tax_return        = np.round((interest_periodic_payment_ann - real_estate_tax) * first_tax_bracket)     # Tax return on paid interest. (Hypotheekrente aftrek)
tax_return        = np.clip(tax_return, 0, max(tax_return))                 # [€/m] Cap tax return, tax benefit can not go negative

net_mortgage_periodic_payment_ann   = total_periodic_payment_ann - tax_return

      
                                                         
#%% [H]         - FAMILY BANK

pr("Annuity Mortgage loan:" + '\n')

pr("8) Monthly Mortgage Payment       =  " + "€ "    + str(round(total_periodic_payment_ann, 0)) + '\n')  # [€] Monthly mortgage payment, this goes into the ownership of the house
pr("      Initial Interest Payment    =  " + "€ "    + str(round(interest_periodic_payment_ann[0], 0 ))) 
pr("      Initial Principal Payment   =  " + "€ "    + str(round(principal_periodic_payment_ann[0], 0)) + '\n') #  
pr("      Initial Net Mortgage (incl tax return)   =  " + "€ "    + str(round(total_periodic_payment_ann - tax_return[0], 0)) + '\n')  
    
if family_loan > 0:

    pr("   *)  Tax return family bank       =    " + "€    " + str(round( - tax_return_family_interest/12, 2)) )
    pr("   **) Monthly net payment          =    " + "€   "  + str(round(total_periodic_payment_ann - tax_return_family_interest/12, 2)) +  3*'\n')
    
    
#%% [I]            - INFLATION 
    
 # Inflation 
inflation                   = -1.92                                     # [%/y] Negative value. Expected yearly inflation over mortgage lifetime (23y avarage). 
inflation_month             = (1 + inflation/100)**(1/12) -1            # [%/month]
inflation_monthly           = (1 - inflation_month) **months_ann        # [%/month] Accumulated over mortgage lifetime

levies                      = levies * np.ones(int(mortgage_payment_periods_ann))                            # [€/month] Monthly maintenance reservation budget (VVE), opstalverzekering
operational                 = operational * np.ones(int(mortgage_payment_periods_ann)) * inflation_monthly   # [€/month]
total_periodic_payment_ann  = total_periodic_payment_ann * np.ones(int(mortgage_payment_periods_ann))

# Calculate amount paid over mortgage lifetime
pr("9) Total amount paid over lifetime   = € " + str(  total_periodic_payment_ann[0] * months_ann[-1]))

    
#%% [J]         - VISUALIZATION
# Plot 1
    
fig = plt.figure()
ax  = fig.add_subplot(1, 1, 1)

fig.set_size_inches(10,10)

plt.plot( net_mortgage_periodic_payment_ann     , color="black"    , label="Total (incl tax return)" , linewidth = 4.5)
plt.plot( total_periodic_payment_ann            , color="gray"     , label="Total (excl tax return)" , linewidth = 2.5)
plt.plot( principal_periodic_payment_ann        , color="blue"     , label="Principal"               , linewidth = 3.0)
plt.plot( interest_periodic_payment_ann         , color="red"      , label="Interest"                , linewidth = 3.0)  
plt.plot( levies                                , color="orange"   , label="Levies"                  , linewidth = 3.0)


plt.title('Monthly payments Annuity mortgage'   , fontsize = 25)
plt.xlabel('Year'                               , fontsize = 20)
plt.ylabel('Euro/month  [€/m]'                  , fontsize = 20)
plt.ylim(0 , np.max(total_periodic_payment_ann) + 200 )

plt.xlim(0 , mortgage_payment_periods_ann)
plt.xticks(12*np.arange(mortgage_payment_periods_ann/12), np.arange(years_ann))     # Convert months to years on x axis

major_ticks_y = np.arange(0,np.max(total_periodic_payment_ann) + 200 , 500)
minor_ticks_y = np.arange(0,np.max(total_periodic_payment_ann) + 200 , 100)


ax.set_yticks(major_ticks_y)
ax.set_yticks(minor_ticks_y, minor=True)

# And a corresponding grid
ax.grid(which='both')

# Or if you want different settings for the grids:
ax.grid(which='major', color='#CCCCCC', linestyle='--')
ax.grid(which='minor', color='#CCCCCC', linestyle=':')
        
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0. , fontsize = 15)
plt.show()

        
 #%%       
# plot 2   Principal and ownership over lifetime   
fig = plt.figure()
ax  = fig.add_subplot(1, 2, 1)

fig.set_size_inches(14,6)
        
plt.plot( remaining_principal_ann/1000    , color="black"   , label="Remaining principal" , linewidth = 3.5)      
plt.plot( principal_accumulated_ann/1000  , color="blue"    , label="Principal paid accumulated" , linewidth = 3.5)


plt.title('Principal over lifetime'   , fontsize = 25)
plt.xlabel('Year'                     , fontsize = 20)
plt.ylabel('Euro [€  X1000]'          , fontsize = 20)
  
plt.xlim(0 , mortgage_payment_periods_ann)

plt.xticks(12*np.arange(mortgage_payment_periods_ann/12), np.arange(years_ann))     # Convert months to years on x axis


major_ticks_y = np.arange(0,np.max(total_periodic_payment_ann) + 200 , 500)
minor_ticks_y = np.arange(0,np.max(total_periodic_payment_ann) + 200 , 100)


# And a corresponding grid
ax.grid(which='both')

# Or if you want different settings for the grids:
ax.grid(which='major', color='#CCCCCC', linestyle='--')
ax.grid(which='minor', color='#CCCCCC', linestyle=':')     
        
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0. , fontsize = 15)
plt.show()


#%%      
# plot 3   Accumulated payments per month   
fig = plt.figure()
ax  = fig.add_subplot(1, 1, 1)

fig.set_size_inches(8,6)
        
plt.plot( principal_accumulated_ann/1000   , color="black"  , label="Principal", linewidth = 3.5)      
plt.plot( interest_accumulated_ann/1000    , color="red"    , label="Interest" , linewidth = 3.5) 

plt.title('Accumulated payments per year '  , fontsize = 25)
plt.xlabel('Year'                           , fontsize = 20)
plt.ylabel('Euro [€  X1000]'                , fontsize = 20)
  
plt.xlim(0 , mortgage_payment_periods_ann)
#plt.ylim(0, remaining_principal_ann)
plt.xticks(12*np.arange(mortgage_payment_periods_ann/12), np.arange(years_ann))     # Convert months to years on x axis

major_ticks_y = np.arange(0,np.max(total_periodic_payment_ann) + 200 , 500)
minor_ticks_y = np.arange(0,np.max(total_periodic_payment_ann) + 200 , 100)

# And a corresponding grid
ax.grid(which='both')

# Or if you want different settings for the grids:
ax.grid(which='major', color='#CCCCCC', linestyle='--')
ax.grid(which='minor', color='#CCCCCC', linestyle=':')     
        
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0. , fontsize = 15)
plt.show()


#%% [K]             - RISING HOUSING PRICES AND UNDERWATER MORTGAGES

# Future value equity
yearly_growth_rate_month    = (1 + yearly_growth_rate/100)**(1/12) -1       # [%/month]


home_increase_ann           = home_value * (1 + yearly_growth_rate_month) ** months_ann 
future_equity_ann           = home_increase_ann - home_value                            # [€] (Overwaarde)
future_equity_net_ann       = future_equity_ann         
home_ownership              = future_equity_ann + principal_accumulated_ann

# Plot
fig = plt.figure()
ax  = fig.add_subplot(1, 1, 1)
fig.set_size_inches(8,6)

  
if yearly_growth_rate/100 > mortgage_rate_ann:  # If yearly growth rate > mortgage interest an extra 'return' is received each year
    
    plt.plot( future_equity_net_ann/1000 + principal_accumulated_ann/1000     , color="green"  , label="Future valuation of property  "  , linewidth = 3.5)         
    plt.plot( future_equity_net_ann/1000 , color="blue"             , label="Future return on investment" , linewidth = 3.5) 
    plt.plot( future_equity_ann_inflation/1000 , color="steelblue"  , label="Future return (inflation adjusted)" , linewidth = 3.5) 
   

elif yearly_growth_rate <0:

    df = pd.DataFrame((home_ownership/1000), columns=['cum_profit'])
    df.cum_profit.where(df.cum_profit.ge(0), np.nan).plot(color='green',    linewidth = 3.5, label='Mortgage total value')
    df.cum_profit.where(df.cum_profit.lt(0), np.nan).plot(color='red',      linewidth = 3.5, label='Mortgage underwater')
    
else:
    plt.plot( future_equity_net_ann/1000 + principal_accumulated_ann/1000,  color="green"  , label="Future valuation of property"  , linewidth = 3.5)      
  
plt.title('Future valuation '   , fontsize = 25)
plt.xlabel('Year'               , fontsize = 20)
plt.ylabel('Euro [€  X1000]'    , fontsize = 20)

plt.xlim(0 , mortgage_payment_periods_ann)

plt.xticks(12*np.arange(mortgage_payment_periods_ann/12), np.arange(years_ann))     # Convert months to years on x axis

major_ticks_y = np.arange(0,np.max(total_periodic_payment_ann) + 200 , 500)
minor_ticks_y = np.arange(0,np.max(total_periodic_payment_ann) + 200 , 100)

ax.grid(which='both')

# Or if you want different settings for the grids:
ax.grid(which='major', color='#CCCCCC', linestyle='--')
ax.grid(which='minor', color='#CCCCCC', linestyle=':') 
      
ax.text(0.05, 0.95, 'Yearly growth rate [%] =', transform=ax.transAxes, fontsize=14, verticalalignment='top')
ax.text(0.45, 0.95, yearly_growth_rate  , transform=ax.transAxes, fontsize=14, verticalalignment='top')

        
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0. , fontsize = 15)
plt.show()


#%% [L]             - MONTHLY NET EXPENSES

fig = plt.figure()
ax  = fig.add_subplot(1, 1, 1)

fig.set_size_inches(10,10)

plt.plot( net_mortgage_periodic_payment_ann     , color="black"    , label="Total (incl tax return)" , linewidth = 4.0)
plt.plot( total_periodic_payment_ann            , color="gray"     , label="Total (excl tax return)" , linewidth = 2.5)
plt.plot( principal_periodic_payment_ann        , color="blue"     , label="Principal"               , linewidth = 3.0)
plt.plot( interest_periodic_payment_ann         , color="red"      , label="Interest"                , linewidth = 3.0)  
plt.plot( levies                                , color="orange"   , label="Levies"                  , linewidth = 3.0)
plt.plot( operational                           , color="green"    , label="Operational costs"       , linewidth = 3.0)
plt.plot( net_mortgage_periodic_payment_ann + operational , color="navy"    , label="Monthly net expenses"       , linewidth = 4.5)


plt.title('Monthly Net Expenses'    , fontsize = 25)
plt.xlabel('Year'                   , fontsize = 20)
plt.ylabel('Euro/month  [€/m]'      , fontsize = 20)
plt.ylim(0 , np.max(total_periodic_payment_ann) + 200 )

plt.xlim(0 , mortgage_payment_periods_ann)
plt.xticks(12*np.arange(mortgage_payment_periods_ann/12), np.arange(years_ann))     # Convert months to years on x axis


major_ticks_y = np.arange(0,np.max(net_mortgage_periodic_payment_ann + operational) + 200 , 500)
minor_ticks_y = np.arange(0,np.max(net_mortgage_periodic_payment_ann + operational) + 200 , 100)


ax.set_yticks(major_ticks_y)
ax.set_yticks(minor_ticks_y, minor=True)

# And a corresponding grid
ax.grid(which='both')

# Or if you want different settings for the grids:
ax.grid(which='major', color='#CCCCCC', linestyle='--')
ax.grid(which='minor', color='#CCCCCC', linestyle=':')
        
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0. , fontsize = 15)
plt.show()

###############################################################################
#%%           ========= End Script ========= 
    
elapsed_s = time.time() - t       # Stop timer
if elapsed_s < 60:
    pr('\n','      Elapsed time =',("%.5f" % elapsed_s),'[s]','\n')
if elapsed_s > 60:
    pr('       Elapsed time =',str(datetime.timedelta(seconds=elapsed_s)),'[h]')  
