<?php
session_start();
 
if(!isset($_SESSION["loggedin"]) || $_SESSION["loggedin"] !== true){
    header("location: login.php");
    exit;
}
?>

<head>

    <link href="contact/fcf-assets/css/fcf.default.css" rel="stylesheet">

</head>

<?php require "template/header.php" ?>

<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <a class="navbar-brand" href="#">
        <img src="images/search.png" width="30" height="30" class="d-inline-block align-top" alt="">
        Supply chain Management
    </a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
        <li class="nav-item">
            <a class="nav-link" href="index.php">Home <span class="sr-only">(current)</span></a>
        </li>
        <li class="nav-item active">
            <a class="nav-link" href="contact.php">Contact </a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="about.php">About </a>
        </li>
        </ul>
        <li class="nav-item dropdown" style="list-style-type: none;">
        <a class="nav-link dropdown-toggle btn btn-outline-info" href="#" id="navbarDropdownMenuLink" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            <?php echo htmlspecialchars($_SESSION["username"]); ?>
        </a>
        <div class="dropdown-menu dropdown-menu-right" aria-labelledby="navbarDropdownMenuLink">
          <a class="dropdown-item" href="reset-password.php">Reset password</a>
          <a class="dropdown-item" href="logout.php">Logout</a>
        </div>
      </li>
    </div>
    
</nav>
<br><br>

<body>


    <!-- the lines below are needed -->
    <div style="max-width:500px;padding:30px">
        <div id="fcf-form">
            <form class="fcf-form-class" id="freeversion" method="post" action="fcf-assets/fcf.process.php">

                <div class="field">
                    <label for="Name" class="label has-text-weight-normal">Your name</label>
                    <div class="control">
                        <input type="text" name="Name" id="Name" class="input is-full-width" maxlength="100"
                            data-validate-field="Name">
                    </div>
                </div>
                <div class="field">
                    <label for="Email" class="label has-text-weight-normal">Your email address</label>
                    <div class="control">
                        <input type="email" name="Email" id="Email" class="input is-full-width" maxlength="100"
                            data-validate-field="Email">
                    </div>
                </div>
                <div class="field">
                    <label for="Message" class="label has-text-weight-normal">Your message</label>
                    <div class="control">
                        <textarea name="Message" id="Message" class="textarea" maxlength="3000" rows="5" 
                        data-validate-field="Message"></textarea>
                    </div>
                </div>
                <div id="fcf-status" class="fcf-status"></div>
                <div class="field">
                    <div class="buttons">
                        <button id="fcf-button" type="submit" class="button is-link is-medium">Send Message</button>
                    </div>
                </div>
            </form>
        </div>
        <div id="fcf-thank-you" style="display:none">
            <!-- Thank you message goes below -->
            <strong>Thank you</strong>
            <p>Thanks for contacting us, we will get back in touch with you soon.</p>
            <!-- Thank you message goes above -->
        </div>
    </div>
    <script src="fcf-assets/js/fcf.just-validate.min.js"></script>
    <script src="fcf-assets/js/fcf.form.js"></script>
    <!-- the lines above are needed -->


</body>

<?php require "template/footer.php" ?>