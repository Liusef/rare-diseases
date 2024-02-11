import React from 'react';
import styled from 'styled-components';

const StyledButton = styled.button`
  transition: .1s;
  display: flex;
  width: fit-content;
  padding: 10px 30px;
  justify-content: center;
  align-items: center;
  gap: 10px;
  border-radius: 2px;
  border: 2px solid #000;
  box-shadow: 4px 4px 0px 0px black;
  color: black;
  font-weight: 600;

  &:hover {
    transform: translate(4px, 4px);
    transition: .1s;
    box-shadow: 0px 0px 0px 0px black;
    border: 2px solid #000;
  }

  &:active {
    background: black;
    color: white;
  }
`;

const Button = ({ text, onClick, color, textColor }) => {
  
  if (!color) {
    color = "#FFFFFF"
  }

  if (!textColor) {
    textColor = "000000"
  }

  return (
    <StyledButton onClick={onClick} style={{backgroundColor: color, color: textColor}}>{text}</StyledButton>
  );
};

export default Button;
