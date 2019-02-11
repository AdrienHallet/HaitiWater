% http://ctan.mirrors.hoobly.com/macros/latex/doc/clsguide.pdf
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{eplmastersthesis_FR}[2016/05/21 EPL Master''s Thesis class]

\LoadClass[11pt, a4paper, openright]{report}

% Usefull packages
\usepackage[utf8x]{inputenc}
\usepackage[french]{babel}

\RequirePackage{microtype} % Improves typography
\RequirePackage[T1]{fontenc}
\RequirePackage{lmodern}
\RequirePackage[pdftex]{graphicx}
\RequirePackage{graphics}
\RequirePackage{color}
\definecolor{UCLblue}{cmyk}{1.00,0.68,0.00,0.54}
\definecolor{EPLblue}{cmyk}{0.70,0.30,0.00,0.00}
\RequirePackage[top=2.5cm,bottom=2.5cm,left=2.5cm,right=2.5cm]{geometry}
\DeclareTextSymbol{\degre}{T1}{6}

\RequirePackage{etoolbox}
\newcommand{\subtitle}[1]{\def\@subtitle{#1}}
\newcommand{\secondauthor}[1]{\def\@secondauthor{#1}}
\newcommand{\thirdauthor}[1]{\def\@thirdauthor{#1}}
\newcommand{\supervisor}[1]{\def\@supervisor{#1}}
\newcommand{\cosupervisor}[1]{\def\@cosupervisor{#1}}
\newcommand{\speciality}[1]{\def\@speciality{#1}}
\newcommand{\options}[1]{\def\@myoptions{#1}}
\newcommand{\readerone}[1]{\def\@readerone{#1}}
\newcommand{\readertwo}[1]{\def\@readertwo{#1}}
\newcommand{\readerthree}[1]{\def\@readerthree{#1}}
\newcommand{\years}[1]{\def\@years{#1}}

% Création de la page de titre
\renewcommand{\maketitle}
	{\begin{titlepage}
	\newgeometry{top=1.25cm,bottom=1.25cm,left=1.25cm,right=1.25cm}
	\begin{center}
		\includegraphics[scale=1]{EPL_TFEbanner.jpg}
	\end{center}
	\vspace*{9pt}
	\begin{flushright}
		\color{UCLblue} \fontfamily{phv} \selectfont
		{\huge \@title} \\
		\vspace*{12pt}
		\ifdef{\@subtitle}{\Large \@subtitle}{$ $} \\
		\vspace*{12pt}
		\large M\'{e}moire pr\'{e}sent\'{e} par \\
		\textbf{\@author}% avoid space before comma
		\ifdef{\@secondauthor}{\textbf{, \@secondauthor}}{}% avoid space before comma
		\ifdef{\@thirdauthor}{\textbf{, \@thirdauthor}}{}
		\\
		\vspace*{12pt}
		en vue de l'obtention du grade de Master \\
		\textbf{\@speciality}\\
		\ifdef{\@myoptions}{\textit{Option(s): \@myoptions}}{$ $}\\
		\vspace*{12pt}
		Promoteur(s)\\
		\textbf{\@supervisor}% avoid space before comma
		\ifdef{\@cosupervisor}{\textbf{, \@cosupervisor}}{}
		\\
		\vspace*{12pt}
		Lecteur(s) \\
		\textbf{\@readerone, \@readertwo}
		\ifdef{\@readerthree}{\textbf{, \@readerthree}}{}
		\\
		\vspace*{12pt}
		Ann\'{e}e acad\'{e}mique \@years \\
	\end{flushright}
	\vspace*{6pt}
	\color{EPLblue}{\rule{18.5cm}{8.25cm}}
  \end{titlepage}
}

% Front cover page
\newcommand{\frontpage}
{
	\maketitle
	\thispagestyle{empty}
}

% Back cover page
\newcommand{\backcoverpage}
{
  \newpage
  \thispagestyle{empty}
  \newgeometry{top=1.25cm,bottom=1.25cm,left=1.25cm,right=1.25cm}
  \vspace*{17.75cm}
  \noindent \footnotesize \color{UCLblue} \fontfamily{phv} \selectfont Rue Archim\`{e}de, 1 bte L6.11.01, 1348 Louvain-la-Neuve ~ ~ \color{EPLblue} \textbf{www.uclouvain.be/epl} \\
  \vspace*{6pt}
  \textcolor{EPLblue}{\rule{18.5cm}{8.25cm}}
}

\endinput
