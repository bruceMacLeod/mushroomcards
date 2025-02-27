import React from 'react';
import './HelpModal.css';

const HelpModal = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="help-dialog-container">
      <div className="help-dialog">
        <div className="help-dialog-header">
          <h2>Help</h2>
          <button className="close-dialog-button" onClick={onClose}>×</button>
        </div>

        <div className="help-dialog-content">
          <h3>Overview</h3>
          <p>
            A tool to help identify and pronounce the scientific names of mushrooms. Flash card decks
            include mushrooms from MMA forays and user defined decks. You can also load in your own
            load with an appropriately designed Comma Separated Value (CSV) file.
          </p>

          <h3>Quick Tips</h3>
          <ul className="help-list">
            <li>
              <strong>Get the name of a Mushroom you do not know: </strong>
              Click on the Check Answer three times
            </li>
            <li>
              <strong>Make the image larger: </strong>
              Click on the image and it will open a larger one
            </li>
            <li>
              <strong>Load another Flashcard deck: </strong>
              Click Manage button in Upper right hand corner, then you can
              choose a deck from MMA forays or a User submitted deck
            </li>
            <li>
              <strong>Pronunciation: </strong>
              English Scientific Latin was chosen for pronunciation. Sometimes, it can take a while as it is going out to the Google Gemini LLM.
            </li>
            <li>
              <strong>Hints: </strong>
              Shows all the scientific names in the flashcard deck. Selecting hint will submit name for
              identification check.
            </li>
            <li>
              <strong>Information sources for decks: </strong>
              So far, iNaturalist and MycoQuebec
            </li>
            <li>
              <strong>Looking for a different style quiz program for mushrooms: </strong>
              Choose quiz tab in
              <a href="https://www.mycoquebec.org/index.php" target="_blank" rel="noopener noreferrer">
                {" "}https://www.mycoquebec.org/index.php
              </a>
            </li>
            <li>
              <strong>How to make a CSV file: </strong>
              Spreadsheet program (Excel, Numbers, Google Sheets) and then export
            </li>
          </ul>

          <h3>Format of the CSV file (an example):</h3>
          <div className="table-container">
            <table className="csv-table">
              <thead>
                <tr>
                  <th>scientific_name</th>
                  <th>common_name</th>
                  <th>image_url</th>
                  <th>attribution</th>
                  <th>taxa_url</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Flammulina velutipes</td>
                  <td>Velvet Foot</td>
                  <td className="break-word">https://static.inaturalist.org/photos/98124470/medium.jpg</td>
                  <td>(c) Melissa Beth Dude Duhaime, all rights reserved</td>
                  <td className="break-word">https://www.inaturalist.org/taxa/67594-Flammulina-velutipes</td>
                </tr>
              </tbody>
            </table>
          </div>

          <p>
            <strong>An example of a CSV file: </strong>
            <a
              href="https://github.com/bruceMacLeod/mushroomcards/blob/master/backend/data/uploads/intro-obs-myco.csv"
              target="_blank"
              rel="noopener noreferrer"
            >
              https://github.com/bruceMacLeod/mushroomcards/blob/master/backend/data/uploads/intro-obs-myco.csv
            </a>
          </p>

          <p>
            <strong>Could you make a deck of something other than mushrooms? </strong> Sure!
          </p>

          <p>
            <strong>Source code </strong> <a
              href="https://github.com/bruceMacLeod/mushroomcards"
              target="_blank"
              rel="noopener noreferrer"
            >
              https://github.com/bruceMacLeod/mushroomcards
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default HelpModal;