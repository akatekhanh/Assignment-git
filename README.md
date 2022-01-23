
# Task 1

# Task 2:
    - program.py -> let see: Program.get_history_FX_rate

# Task 3:
    - 3a:
        utils.py -> utils.get_currency_code
        Scrape data from https://www.iban.com/currency-codes and save data to data/currency_code.csv
    - 3b:
        utils.py -> utils.get_score_world_happiness_index
        Scrape data from https://en.wikipedia.org/wiki/World_Happiness_Report#2019_report and save data to data/world_happiness_report.csv

# Task 4:
    - python.py task_4.py

# Task 5: uncomment to run
    - Program.value_asset()

# Task 6: 
    - Program.consolidate_asset()

# Task 7:
    - Program.plot_the_change_in_value(year, currency_code)

# Task 8:
    - Program.prove_historically_FX_rate()


# Docker
## To build docker
    docker build -t assignment  .    

## To run docker
    docker run -it assignment bash
    python program.py 
