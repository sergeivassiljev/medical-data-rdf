import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import axios from "axios";
import { Form, Container, Row, Col, Button, Card, Spinner } from "react-bootstrap";
import { motion } from "framer-motion";

function App() {
  const [text, setText] = useState("");
  const [response, setResponse] = useState({
    generated_rdf: "",
    translated_rdf: "",
  });
  const [showTranslated, setShowTranslated] = useState(false);
  const [history, setHistory] = useState([]);
  const [activeHistoryIndex, setActiveHistoryIndex] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true); 
    try {
      const response = await axios.post("http://localhost:5000/generate_rdf", {
        text,
      });
      setResponse(response.data);
      setHistory((prevHistory) => [
        ...prevHistory,
        { text, response: response.data },
      ]);
    } catch (error) {
      console.error("Error while sending:", error);
    } finally {
      setIsLoading(false); 
    }
  };

  function HistoryItem({ item, index, onClick, isActive }) {
    return (
      <motion.div
        initial={{ x: 50, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ duration: 0.5 }}
        className={`history-item mb-2 p-2 bg-light border rounded ${
          isActive ? "bg-info text-white" : ""
        }`}
        onClick={() => onClick(item)}
      >
        {item.text.substring(0, 50)}...
      </motion.div>
    );
  }

  return (
    <Container className="mt-5">
      <Row className="justify-content-md-center">
        <Col lg={8}>
          <Card className="mb-4 shadow-sm">
            <Card.Body>
              <h2 className="mb-4">
               Generate and translate RDF from medical text
              </h2>
              <form onSubmit={handleSubmit}>
                <Form.Group>
                  <Form.Label>Enter medical data:</Form.Label>
                  <Form.Control
                    as="textarea"
                    rows="4"
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                  />
                </Form.Group>
                <Button variant="primary" type="submit" className="mt-2">
                  Generate RDF
                </Button>
              </form>
              {isLoading && (
                <div className="d-flex justify-content-center my-2">
                  <Spinner animation="border" role="status">
                    <span className="sr-only">...</span>
                  </Spinner>
                </div>
              )}
            </Card.Body>
          </Card>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            <Form>
              <Form.Check
                type="switch"
                id="custom-switch"
                label={
                  showTranslated ? "Translated RDF" : "Generated RDF"
                }
                checked={showTranslated}
                onChange={() => setShowTranslated(!showTranslated)}
                className="mb-3"
              />
            </Form>
            <Card className="shadow-sm">
              <Card.Body>
                <Card.Title>
                  {showTranslated
                    ? "Translated RDF:"
                    : "Generated RDF:"}
                </Card.Title>
                <Card.Text>
                  {showTranslated
                    ? response.translated_rdf
                    : response.generated_rdf}
                </Card.Text>
              </Card.Body>
            </Card>
          </motion.div>
        </Col>
        <Col lg={4}>
          <div className="history-panel">
            <h5>History of requests</h5>
            {history.map((item, index) => (
              <HistoryItem
                key={index}
                index={index}
                item={item}
                isActive={index === activeHistoryIndex}
                onClick={(selectedItem) => {
                  setResponse(selectedItem.response);
                  setActiveHistoryIndex(index);
                }}
              />
            ))}
          </div>
        </Col>
      </Row>
    </Container>
  );
}

export default App;
