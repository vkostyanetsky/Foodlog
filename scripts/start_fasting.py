import modules.fasting_journal_wrapper as fasting_journal_wrapper

fasting_length = input("Продолжительность голодания (в часах): ")

message = fasting_journal_wrapper.start_fasting(fasting_length)

if message != '':
    print(message)