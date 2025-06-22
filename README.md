# dm-data-contextual-replacer
Replaces data based on contextual keywords identified nearby. For instance, if 'salary' or 'income' appears within N words of a number, replace the number with a masked value. Requires a pre-defined list of contextual keywords. - Focused on Tools designed to generate or mask sensitive data with realistic-looking but meaningless values

## Install
`git clone https://github.com/ShadowGuardAI/dm-data-contextual-replacer`

## Usage
`./dm-data-contextual-replacer [params]`

## Parameters
- `-h`: Show help message and exit
- `--input`: The input text to process.
- `--keywords`: Comma-separated list of contextual keywords.
- `--window_size`: No description provided
- `--replacement_value`: The value to replace matched data with. If not provided, a random float is generated.
- `--faker_locale`: No description provided
- `--log_level`: No description provided

## License
Copyright (c) ShadowGuardAI
