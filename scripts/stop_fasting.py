import modules.fasting_journal_wrapper  as fasting_journal_wrapper

message = fasting_journal_wrapper.stop_fasting()

if message != '':
    print(message)