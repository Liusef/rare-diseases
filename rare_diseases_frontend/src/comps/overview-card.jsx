import React from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from './Button.jsx';

const payload = {
  results: [
    {
      name: 'Disease',
      url: 'https://example.com',
      affected_text: 'ur mom',
      symptom_text: 'ligma',
      prediction: 0.98
    },
    {
      name: 'Disease',
      url: 'https://example.com',
      affected_text: 'ur mom',
      symptom_text: 'ligma',
      prediction: 0.2
    }
  ]
}

function OverviewCard(result) {
  return (
    <div class="container">
      <p>{result.name}</p>
      <p>{result.affected_text}</p>
      <p>{}</p>
      <p></p>
    </div>
  );
}

export default OverviewCard