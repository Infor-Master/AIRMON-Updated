package email

import (
	"bytes"
	"fmt"
	"html/template"
	"log"
	"net/smtp"
	"os"
)

func SendInvite(emailTo string, token string) {

	from := os.Getenv("EMAIL_USER")
	to := []string{emailTo}
	password := os.Getenv("EMAIL_PASS")
	smtpHost := os.Getenv("SMTP_HOST")
	smtpPort := os.Getenv("SMTP_PORT")

	auth := smtp.PlainAuth("", from, password, smtpHost)

	t, _ := template.ParseFiles("invite.html")

	var body bytes.Buffer

	mimeHeaders := "MIME-version: 1.0;\nContent-Type: text/html; charset=\"UTF-8\";\n\n"

	body.Write([]byte(fmt.Sprintf("Subject: Invite to AIRMON platform \n%s\n\n", mimeHeaders)))

	t.Execute(&body, struct {
		Email string
		Token string
		Link  string
	}{
		Email: emailTo,
		Token: token,
		Link:  os.Getenv("ADDRESS"),
	})

	err := smtp.SendMail(smtpHost+":"+smtpPort, auth, from, to, body.Bytes())
	if err != nil {
		log.Println(err)
		return
	}
}
