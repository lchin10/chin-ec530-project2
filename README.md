# chin-ec530-project2

## Smart Document Analyzer (mainly cloud)

## Mission:

Analyze Catalog Search summarize Topics

## User Stories:

  - I should login to a secure service to upload my content
  - I should be able to upload documents
  - I should be able to upload PDFs or images.  The application should translate my documents to text
  - I want the service to tag all my documents and paragraphs within every document with the keywords and know the topics each document cover
  - I should be able to access different paragraphs of different documents based on keywords
  - I should be able to to find all positive, neutral and negative paragraphs and sentences
  - Keywords within paragraphs should be searchable in government opendata, wikipedia and media organizations, e.g., NYTimes
  - I should find definition of keywords using open services (e.g., OpenAI)
  - I should be able to get summaries of each document
  - I want to discover content from the WEB to enhance story
  - I want to know all names, locations, institutions and address in my documents.
  - I want to upload different types of files (CSV, DOC, etc.)

## Modules:

**Authorization and Authentication**

**Secure File Uploader/Ingester:**

  - User authentication
  - Upload file
  - Parse file
  - File handler (for different types of files)
  - Image to text (using a ML model)
  - Verify file (make sure it is a certain type/size)
  - Ingest file (prepare video files for editing)
  - Save file (after files are successfully ingested)

**Feed Ingester**

**Output Generator**

**Text NLP Analysis:**

  - Find topics and keywords (for whole text and seperate paragraphs)
  - Negative/positive parser (for sentences and paragraphs)
  - External Search (data and keywords from open services)
  - Text summarization
  - Web content discovery (for story enhancement)
  - Name recognizer (names, locations, institutions and address)
