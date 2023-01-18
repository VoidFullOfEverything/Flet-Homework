import flet as ft
import requests
import bs4
from bs4 import BeautifulSoup


def get_meaning(word, site, datasrc):
    """Get the meaning for a given word from an online dictionary."""
    response = requests.get(site + word)
    if not response.ok:
        if response.status_code == 404:
            print("Word not found")
        else:
            print(f"An error occurred: {response.reason}")
        # exit(255)
        return f"An error occurred: {response.reason}"

    soup = BeautifulSoup(response.text, "html.parser")

    data = soup.find("section", attrs=datasrc).findAll("div")

    meaning = ""
    for line in data:
        meaning = f"{meaning}\n{line.get_text()}"

    return meaning


# Main
def main(page):
    page.title = "Meaning"
    page.window_width=500
    page.window_height=500
    page.scroll = "adaptive"
    
    # When the button is clicked, we display the results of the lookup.
    def btn_click(e):
        # first clear the original text
        
        if not txt_word.value:
            txt_word.error_text = "Please enter a word to lookup"
            page.update()
        else:
            # show the progress bar
            page.splash = ft.ProgressBar()
            btn_click.disabled = True
            page.update()
            # get the entry
            word = txt_word.value
            intro = f"Your word was {word}:\n"
            datasrc = {"data-src": "hc_dict"}
            site = "https://www.thefreedictionary.com/"
            response = get_meaning(word, site, datasrc)
            # Reset the response output view
            response_list.clean()
            response_list.value = f"{intro}{response}"
            page.splash = None
            page.update()

    # Inputs View
    txt_word = ft.TextField(label="What's a word you'd like to learn?",on_submit=btn_click)
    btn = ft.ElevatedButton("Define", on_click=btn_click)
    input_controls = ft.Column(controls=[
        ft.Row(controls=[txt_word, btn] ,
               alignment=ft.MainAxisAlignment.SPACE_EVENLY),
    ])
    page.add(input_controls)
    # Output View
    response_list = ft.Text("")  # ft.Text("")
    page.add(response_list)
    
    page.update()

ft.app(target=main)
