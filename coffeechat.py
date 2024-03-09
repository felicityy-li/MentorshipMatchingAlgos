import csv

# Load mentors and mentees data from CSV files
def load_csv(file_path):
    with open(file_path, encoding='utf8') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data

mentors_data = load_csv('mentors.csv')
mentees_data = load_csv('mentees.csv')

# Define the order of preference for meeting frequency
meeting_frequency_order = {
    "I want to meet up a lot!": 3,
    "Some events and we may meet up occasionally on our own.": 2,
    "Mostly just a few events and whenever they need help.": 1
}

# Map meeting frequency options to their corresponding order
for mentor in mentors_data:
    mentor['Meeting Order'] = meeting_frequency_order.get(mentor['How often would you like to meet and chat with your mentee?'], 0)


for mentee in mentees_data:
    mentee['Meeting Order'] = meeting_frequency_order.get(mentee['How often would you like to meet and chat with your mentor?'], 0)


# Sort mentors and mentees based on meeting frequency order
mentors_data.sort(key=lambda x: x['Meeting Order'], reverse=True)
mentees_data.sort(key=lambda x: x['Meeting Order'], reverse=True)

# Match mentors to mentees based on the specified fields
matched_pairs = []
unmatched_mentees = list(mentees_data)

for mentor in mentors_data:
    mentor_email = mentor['Email address']
    mentor_limit = int(mentor['How many mentees would you like to mentor this term?'])

    while mentor_limit > 0 and unmatched_mentees:
        best_match_score = float('-inf')
        best_match_mentee = None

        for mentee in unmatched_mentees:
            match_score = abs(mentor['Meeting Order'] - mentee['Meeting Order'])
            field_score = sum(
                mentee[field] == mentor[field]
                for field in ['First field', 'Second field', 'Third field']
            )
            total_score = match_score + field_score

            if total_score > best_match_score:
                best_match_score = total_score
                best_match_mentee = mentee

        if best_match_mentee is not None:
            matched_pairs.append((best_match_mentee['First Name'], best_match_mentee['Last Name'], best_match_mentee['Email address'], mentor['First Name'], mentor['Last Name'], mentor_email))
            unmatched_mentees.remove(best_match_mentee)
            mentor_limit -= 1
        else:
            break  # No suitable mentee found for this mentor

# Display the matched pairs
for pair in matched_pairs:
    print(f'Mentee: {pair[0]} {pair[1]} - {pair[2]} | Mentor: {pair[3]} {pair[4]} - {pair[5]}')

# Save matched pairs to CSV
with open('output_matches.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Mentee First Name', 'Mentee Last Name', 'Mentee Email', 'Mentor First Name', 'Mentor Last Name', 'Mentor Email'])
    writer.writerows(matched_pairs)

# Save unmatched mentees to CSV
with open('unmatched_mentees.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Mentee First Name', 'Mentee Last Name', 'Mentee Email'])
    writer.writerows(unmatched_mentees)
