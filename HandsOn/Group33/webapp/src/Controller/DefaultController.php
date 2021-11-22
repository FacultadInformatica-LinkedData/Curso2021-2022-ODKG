<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\HttpFoundation\Request;

class DefaultController extends AbstractController
{
    /**
     * @Route("/", name="mainpage")
     */
    public function index(): Response
    {

        return $this->render('main/index.html.twig', [
            // 'activedocs' => $active,
        ]);
    }
}